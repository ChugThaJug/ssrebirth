import json
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from youtube_transcript_api import YouTubeTranscriptApi
from openai import AsyncOpenAI
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# # Import Paddle SDK correctly
# from paddle_billing import Client as PaddleClient
# from paddle_billing import Environment, Options

from .core.config import settings


# def get_paddle_client():
#     return PaddleClient(
#         settings.PADDLE_API_KEY,
#         options=Options(Environment.SANDBOX if settings.PADDLE_SANDBOX else Environment.PRODUCTION)
#     )

# # Paddle utility functions

# def verify_paddle_signature(request):
#     from paddle_billing.Notifications import Secret, Verifier
#     return Verifier().verify(request, Secret(settings.PADDLE_WEBHOOK_SECRET))

# def get_subscription_status(status):
#     # Map Paddle subscription statuses to your application's statuses
#     status_map = {
#         'active': 'active',
#         'trialing': 'active',
#         'past_due': 'past_due',
#         'paused': 'paused',
#         'canceled': 'cancelled'
#     }
#     return status_map.get(status, 'unknown')

# ... (rest of the existing functions)


# Price token dictionary
price_token = {
    'gpt-4o': {'input': 5/1000000, 'output': 15/1000000},
    'gpt-4o-2024-08-06': {'input': 2.5/1000000, 'output': 10/1000000},
    'gpt-4o-mini-2024-07-18': {'input': 0.15/1000000, 'output': 0.6/1000000},
    'llama3-8b-8192': {'input': 0.05 / 1000000, 'output': 0.08 / 1000000},
    'llama3-70b-8192': {'input': 0.59 / 1000000, 'output': 0.79 / 1000000},
    'claude-3-5-sonnet-20240620': {'input': 3/1000000, 'output': 15/1000000},
    'claude-3-haiku-20240307': {'input': 0.25/1000000, 'output': 1.25/1000000},
}

async def get_youtube_transcript(video_id):
    return YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])


async def get_video_details(video_id):
    youtube_api_key = os.getenv("YOUTUBE_API_KEY")
    if not youtube_api_key:
        raise ValueError("YouTube API key is not set")

    youtube = build('youtube', 'v3', developerKey=youtube_api_key)

    try:
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()

        if not response['items']:
            raise ValueError(f"No video found with id: {video_id}")

        video_data = response['items'][0]
        snippet = video_data['snippet']

        return {
            'title': snippet['title'],
            'description': snippet['description'],
            'channel_title': snippet['channelTitle'],
            'thumbnail_url': snippet['thumbnails']['high']['url'],
            'published_at': snippet['publishedAt'],
            'view_count': video_data['statistics'].get('viewCount', 0),
            'like_count': video_data['statistics'].get('likeCount', 0),
            'duration': video_data['contentDetails']['duration']
        }

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        raise
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise



async def call_llm(client, model, system_prompt, prompt, temperature=0, seed=42, response_format=None, max_tokens=5000):
    response = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        model=model,
        temperature=temperature,
        seed=seed,
        response_format=response_format,
        max_tokens=max_tokens
    )

    nb_input_tokens = response.usage.prompt_tokens
    nb_output_tokens = response.usage.completion_tokens
    price = nb_input_tokens * price_token[model]['input'] + nb_output_tokens * price_token[model]['output']

    print(f"input tokens: {nb_input_tokens}; output tokens: {nb_output_tokens}, price: {price}")

    return response.choices[0].message.content, nb_input_tokens, nb_output_tokens, price

async def transcript_to_paragraphs(transcript, llm_client, llm_model, chunk_size=5000, progress=None):
    transcript_as_text = ' '.join([s['text'] for s in transcript])

    paragraphs = []
    last_paragraph = ""

    total_nb_input_tokens, total_nb_output_tokens, total_price = 0, 0, 0
    
    nb_chunks = int(len(transcript_as_text) / chunk_size) + 1
    progress_i = 0
    print(f"Number of chunks: {nb_chunks}")

    system_prompt = """
    You are a helpful assistant.
    Your task is to improve the user input's readability: add punctuation if needed and remove verbal tics, and structure the text in paragraphs separated with '\n\n'.
    Keep the wording as faithful as possible to the original text. 
    Put your answer within <answer></answer> tags.
    """

    for i in range(0, len(transcript_as_text), chunk_size):
        chunk = last_paragraph + " " + transcript_as_text[i:i + chunk_size]
        
        if progress is not None:
            progress_i += 1
            progress(progress_i/nb_chunks, desc="Processing")
        
        response_content, nb_input_tokens, nb_output_tokens, price = await call_llm(
            llm_client, llm_model, system_prompt, chunk, temperature=0.2, seed=42
        )

        if not "</answer>" in response_content:
            response_content += "</answer>"
            
        pattern = re.compile(r'<answer>(.*?)</answer>', re.DOTALL)
        response_content_edited = pattern.findall(response_content)
        
        if len(response_content_edited) > 0:
            response_content_edited = response_content_edited[0]
            paragraphs_chunk = response_content_edited.strip().split('\n\n')
            last_paragraph = paragraphs_chunk[-1]
            paragraphs += paragraphs_chunk[:-1]

        total_nb_input_tokens += nb_input_tokens
        total_nb_output_tokens += nb_output_tokens
        total_price += price

    paragraphs += [last_paragraph]
    paragraphs_dict = [{'paragraph_number': i, 'paragraph_text': paragraph} for i, paragraph in enumerate(paragraphs)]

    return paragraphs_dict, total_nb_input_tokens, total_nb_output_tokens, total_price

def transform_text_segments(text_segments, num_words=50):
    transformed_segments = []
    for i in range(len(text_segments)):
        current_segment = text_segments[i]
        combined_text = " ".join(current_segment['text'].split()[:num_words])
        transformed_segments.append(combined_text)
    return transformed_segments

def add_timestamps_to_paragraphs(transcript, paragraphs, num_words=50):
    transcript_num_words = transform_text_segments(transcript, num_words=num_words)
    paragraphs_start_text = [{"start": p['paragraph_number'], "text": p['paragraph_text']} for p in paragraphs]
    paragraphs_num_words = transform_text_segments(paragraphs_start_text, num_words=num_words)
    
    vectorizer = TfidfVectorizer().fit_transform(transcript_num_words + paragraphs_num_words)
    vectors = vectorizer.toarray()
    
    for i, paragraph in enumerate(paragraphs):
        paragraph_vector = vectors[len(transcript_num_words) + i]
        similarities = cosine_similarity(vectors[:len(transcript_num_words)], paragraph_vector.reshape(1, -1))
        best_match_index = int(np.argmax(similarities))
        
        paragraphs[i]['matched_index'] = best_match_index
        paragraphs[i]['matched_text'] = transcript[best_match_index]['text']
        paragraphs[i]['start_time'] = max(0, int(transcript[best_match_index]['start']) - 2)

    return paragraphs

async def paragraphs_to_toc(paragraphs, llm_client, llm_model, chunk_size=100):
    chapters = []
    number_last_chapter = 0
    total_nb_input_tokens, total_nb_output_tokens, total_price = 0, 0, 0

    system_prompt = """
    You are given a transcript of a course in JSON format as a list of paragraphs, each containing 'paragraph_number' and 'paragraph_text' keys.
    Your task is to group consecutive paragraphs in chapters for the course and identify meaningful chapter titles.
    Format your result in JSON, with a list of dictionaries for chapters, with 'start_paragraph_number':integer and 'title':string as key:value.
    """

    while number_last_chapter < len(paragraphs):
        chunk = paragraphs[number_last_chapter:(number_last_chapter + chunk_size)]
        chunk = [{'paragraph_number': p['paragraph_number'], 'paragraph_text': p['paragraph_text']} for p in chunk]
        chunk_json_dump = json.dumps(chunk)

        content, nb_input_tokens, nb_output_tokens, price = await call_llm(
            llm_client, llm_model, system_prompt, chunk_json_dump,
            temperature=0, seed=42, response_format={"type": "json_object"}
        )

        total_nb_input_tokens += nb_input_tokens
        total_nb_output_tokens += nb_output_tokens
        total_price += price
        
        chapters_chunk = json.loads(content)['chapters']
        if number_last_chapter == chapters_chunk[-1]['start_paragraph_number']:
            break

        chapters += chapters_chunk[:-1]
        number_last_chapter = chapters_chunk[-1]['start_paragraph_number']
        if number_last_chapter >= len(paragraphs) - 5:
            break

    chapters += [chapters_chunk[-1]]
    return chapters, total_nb_input_tokens, total_nb_output_tokens, total_price

def get_chapters(paragraphs, table_of_content):
    chapters = []
    for i, chapter in enumerate(table_of_content):
        if i < len(table_of_content) - 1:
            end_paragraph_number = table_of_content[i + 1]['start_paragraph_number']
            end_time = paragraphs[table_of_content[i + 1]['start_paragraph_number']]['start_time']
        else:
            end_paragraph_number = len(paragraphs)
            end_time = paragraphs[-1]['start_time']

        chapter_data = {
            'num_chapter': i,
            'title': chapter['title'],
            'start_paragraph_number': chapter['start_paragraph_number'],
            'end_paragraph_number': end_paragraph_number,
            'start_time': paragraphs[chapter['start_paragraph_number']]['start_time'],
            'end_time': end_time,
            'paragraphs': [p['paragraph_text'] for p in paragraphs[chapter['start_paragraph_number']:end_paragraph_number]],
            'paragraph_timestamps': [p['start_time'] for p in paragraphs[chapter['start_paragraph_number']:end_paragraph_number]]
        }
        chapters.append(chapter_data)
    return chapters

def convert_seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{remaining_seconds:02}"

def get_result_as_html(chapters, video_id):
    video_embed = f"""
    <iframe width="100%" height="400" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    """

    toc_html = "<h1>Video chapters</h1><p>\n"
    for chapter in chapters:
        from_to = convert_seconds_to_hms(int(chapter['start_time'])) + " - "
        toc_html += f"""{from_to}<a href = "#{chapter['num_chapter']}" >{chapter['num_chapter']+1} - {chapter['title']}</a><br>\n"""

    edited_transcript = "<h1>Structured transcript</h1><p>\n"
    for chapter in chapters:
        edited_transcript += f"""
        <h2><div class="transcript-title-icon" id="{chapter['num_chapter']}">{chapter['num_chapter']+1} - {chapter['title']}</div></h2>
        From {convert_seconds_to_hms(int(chapter['start_time']))} to {convert_seconds_to_hms(int(chapter['end_time']))}
        <p>
        <div class="summary-section">
            <div class="summary-text">
        """
        for paragraph, timestamp in zip(chapter['paragraphs'], chapter['paragraph_timestamps']):
            edited_transcript += f"""
            <div class="row mb-4">
                <div class="col-md-1">
                    {convert_seconds_to_hms(int(timestamp))}
                </div>
                <div class="col-md-11">
                    <p>{paragraph}</p>
                </div>
            </div>"""
        edited_transcript += "</div></div>"

    result_as_html = f"""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <div class="container mt-4">
        <div class="content">
            {video_embed}
        </div>
        <p>
        <div class="content">
            {toc_html}
        </div>
        <p>
        <div class="content">
            {edited_transcript}
        </div>
    </div>"""

    return result_as_html
