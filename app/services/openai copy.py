# app/services/openai.py
from openai import AsyncOpenAI
from app.core.settings import settings
import asyncio
from fastapi import HTTPException
import logging
from typing import Dict, List, Optional, Callable, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.system_prompt = """Process this transcript into clean, well-structured paragraphs.
        Remove verbal tics, add proper punctuation, and organize the content logically.
        Maintain the original meaning and key information."""
        
        # Price rates for different models
        self.price_rates = {
            'gpt-4o': {'input': 5/1000000, 'output': 15/1000000},
            'gpt-4o-2024-08-06': {'input': 2.5/1000000, 'output': 10/1000000},
            'gpt-4o-mini-2024-07-18': {'input': 0.15/1000000, 'output': 0.6/1000000},
            'gpt-4o-mini': {'input': 0.15/1000000, 'output': 0.6/1000000},
            'llama3-8b-8192': {'input': 0.05/1000000, 'output': 0.08/1000000},
            'llama3-70b-8192': {'input': 0.59/1000000, 'output': 0.79/1000000},
            'claude-3-5-sonnet-20240620': {'input': 3/1000000, 'output': 15/1000000},
            'claude-3-haiku-20240307': {'input': 0.25/1000000, 'output': 1.25/1000000},
        }
        self.default_rates = {'input': 0.0001, 'output': 0.0002}

    def calculate_price(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate price based on token usage."""
        model = settings.MODEL
        rates = self.price_rates.get(model, self.default_rates)
        total_price = (
            input_tokens * rates['input'] +
            output_tokens * rates['output']
        )
        return round(total_price, 6)

    async def transcript_to_paragraphs(
        self,
        transcript: List[Dict],
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> Tuple[List[Dict], int, int, float]:
        """Process transcript into paragraphs with progress tracking."""
        total_input_tokens = 0
        total_output_tokens = 0
        total_price = 0
        paragraphs = []
        successful_chunks = 0
        
        # Combine transcript text while keeping track of start times
        text_chunks = []
        current_chunk = {"text": "", "start_time": None}
        current_length = 0
        
        for segment in transcript:
            text = segment["text"].strip()
            if not text:
                continue
                
            # Start new chunk if needed
            if current_length + len(text) > settings.CHUNK_SIZE or not current_chunk["text"]:
                if current_chunk["text"]:
                    text_chunks.append(current_chunk)
                current_chunk = {"text": text, "start_time": float(segment["start"])}
                current_length = len(text)
            else:
                current_chunk["text"] += " " + text
                current_length += len(text) + 1
                
        # Add final chunk if not empty
        if current_chunk["text"]:
            text_chunks.append(current_chunk)
        
        total_chunks = len(text_chunks)
        
        for i, chunk in enumerate(text_chunks):
            if progress_callback:
                progress = (i + 1) / total_chunks * 0.5
                await progress_callback(progress, "Processing transcript chunks")
            
            for attempt in range(settings.MAX_RETRIES):
                try:
                    response = await self.client.chat.completions.create(
                        model=settings.MODEL,
                        messages=[
                            {"role": "system", "content": self.system_prompt},
                            {"role": "user", "content": chunk["text"]}
                        ],
                        temperature=0.7,
                        max_tokens=int(len(chunk["text"]) * 1.5)
                    )
                    
                    # Update tokens and price
                    total_input_tokens += response.usage.prompt_tokens
                    total_output_tokens += response.usage.completion_tokens
                    total_price += self.calculate_price(
                        response.usage.prompt_tokens,
                        response.usage.completion_tokens
                    )
                    
                    # Process the response into paragraphs
                    chunk_paragraphs = [p.strip() for p in response.choices[0].message.content.strip().split("\n\n") if p.strip()]
                    
                    if chunk_paragraphs:
                        for j, p in enumerate(chunk_paragraphs):
                            paragraphs.append({
                                "paragraph_number": len(paragraphs),
                                "paragraph_text": p,
                                "start_time": chunk["start_time"]  # Add timestamp from chunk
                            })
                        successful_chunks += 1
                    break  # Break retry loop if successful
                    
                except Exception as e:
                    logger.error(f"Error processing chunk {i} (attempt {attempt + 1}): {str(e)}")
                    if attempt == settings.MAX_RETRIES - 1:
                        logger.warning(f"Failed to process chunk {i} after {settings.MAX_RETRIES} attempts")
                    await asyncio.sleep(settings.RETRY_DELAY)
        
        # Check if we have enough successful chunks
        if successful_chunks < total_chunks * 0.5:  # At least 50% success rate
            logger.error(f"Too many failed chunks: {successful_chunks}/{total_chunks}")
            raise ValueError(f"Failed to process too many chunks ({successful_chunks}/{total_chunks})")
        
        if not paragraphs:
            raise ValueError("No paragraphs were generated")
            
        logger.info(f"Successfully processed {successful_chunks}/{total_chunks} chunks")
        return paragraphs, total_input_tokens, total_output_tokens, total_price

    async def add_timestamps_to_paragraphs(
        self,
        transcript: List[Dict],
        paragraphs: List[Dict],
        num_words: int = 50
    ) -> List[Dict]:
        """Add timestamps to paragraphs using TF-IDF matching."""
        try:
            # Transform transcript segments for TF-IDF
            transcript_segments = [t["text"] for t in transcript]
            vectorizer = TfidfVectorizer(stop_words="english")
            
            # Create TF-IDF matrix for transcript and paragraphs
            tfidf_matrix = vectorizer.fit_transform(transcript_segments + [p["paragraph_text"] for p in paragraphs])
            
            # For each paragraph, find best matching transcript segment
            for i, paragraph in enumerate(paragraphs):
                paragraph_vector = tfidf_matrix[len(transcript_segments) + i]
                similarities = cosine_similarity(tfidf_matrix[:len(transcript_segments)], paragraph_vector)
                best_match_idx = np.argmax(similarities)
                
                # Add timestamp information
                paragraphs[i]["start_time"] = max(0, float(transcript[best_match_idx]["start"]) - 2)
                paragraphs[i]["matched_text"] = transcript[best_match_idx]["text"]
                
            return paragraphs
            
        except Exception as e:
            logger.error(f"Error adding timestamps: {str(e)}")
            raise

async def generate_toc(
        self,
        paragraphs: List[Dict]
    ) -> Tuple[List[Dict], int, int, float]:
        """Generate table of contents from paragraphs."""
        try:
            # Prepare the text
            text = "\n\n".join([p["paragraph_text"] for p in paragraphs])
            total_paragraphs = len(paragraphs)
            
            system_prompt = f"""Create a detailed table of contents for this content.
            
            Instructions:
            1. Identify 3-7 major topics or natural break points
            2. Each chapter should represent a coherent section of content
            3. Make chapter titles clear and descriptive
            4. Ensure chapters are evenly distributed
            
            Format your response as a JSON object with this exact structure:
            {{
                "chapters": [
                    {{"start_paragraph_number": 0, "title": "Introduction"}},
                    {{"start_paragraph_number": N, "title": "Chapter Title"}},
                    ...
                ]
            }}

            The start_paragraph_number must be between 0 and {total_paragraphs-1}.
            Chapters must be in ascending order of start_paragraph_number.
            """

            response = await self.client.chat.completions.create(
                model=settings.MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.7,
                max_tokens=1000,
                response_format={"type": "json_object"}
            )
            
            # Extract and process the response
            toc_content = response.choices[0].message.content
            toc_data = json.loads(toc_content)
            
            # Validate chapter data
            valid_chapters = []
            last_valid_point = -1
            
            for chapter in toc_data.get("chapters", []):
                start_point = chapter.get("start_paragraph_number")
                
                if (start_point is None or 
                    start_point >= total_paragraphs or 
                    start_point <= last_valid_point):
                    logger.warning(f"Skipping invalid TOC entry: {chapter}")
                    continue
                
                valid_chapters.append(chapter)
                last_valid_point = start_point

            return (
                valid_chapters,
                response.usage.prompt_tokens,
                response.usage.completion_tokens,
                self.calculate_price(
                    response.usage.prompt_tokens,
                    response.usage.completion_tokens
                )
            )
            
        except Exception as e:
            logger.error(f"Error generating TOC: {str(e)}")
            return (
                [{"start_paragraph_number": 0, "title": "Complete Content"}],
                0, 0, 0
            )