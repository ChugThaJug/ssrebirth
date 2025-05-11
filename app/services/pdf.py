# app/services/pdf.py
import os
import json
from datetime import datetime
import PyPDF2
from fastapi import HTTPException
from typing import List, Optional
import logging
from app.core.settings import settings
from app.services.openai import OpenAIService

logger = logging.getLogger(__name__)

class PDFService:
    def __init__(self):
        self.openai_service = OpenAIService()

    def validate_pdf(self, file_path: str) -> bool:
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail=f"File not found at path: {file_path}"
            )
        if not file_path.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="File is not a PDF"
            )
        return True

    def extract_text_from_pdf(self, file_path: str) -> Optional[str]:
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                extracted_text = []
                total_chars = 0
                
                for page_num in range(num_pages):
                    if total_chars >= settings.MAX_CHARS:
                        break
                        
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    
                    remaining_chars = settings.MAX_CHARS - total_chars
                    if len(text) > remaining_chars:
                        text = text[:remaining_chars]
                        
                    extracted_text.append(text)
                    total_chars += len(text)
                
                return '\n'.join(extracted_text)
                
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing PDF: {str(e)}"
            )

    def get_pdf_metadata(self, file_path: str) -> dict:
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return {
                    "num_pages": len(pdf_reader.pages),
                    "metadata": dict(pdf_reader.metadata)
                }
        except Exception as e:
            logger.error(f"Error extracting metadata: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error extracting metadata: {str(e)}"
            )

    @staticmethod
    def create_word_bounded_chunks(text: str) -> List[str]:
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1
            if current_length + word_length > settings.CHUNK_SIZE and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = word_length
            else:
                current_chunk.append(word)
                current_length += word_length
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks

class ProcessingJob:
    def __init__(self, job_id: str, filename: str):
        self.job_id = job_id
        self.filename = filename
        self.status = "pending"
        self.progress = 0.0
        self.result_path = None
        self.error = None
        self.pdf_service = PDFService()
        self._save_status()

    def _save_status(self):
        status_path = os.path.join(settings.CACHE_DIR, f"{self.job_id}.json")
        with open(status_path, 'w') as f:
            json.dump({
                "job_id": self.job_id,
                "status": self.status,
                "progress": self.progress,
                "result_path": self.result_path,
                "error": self.error
            }, f)

    @staticmethod
    def load(job_id: str) -> "ProcessingJob":
        status_path = os.path.join(settings.CACHE_DIR, f"{job_id}.json")
        if not os.path.exists(status_path):
            raise HTTPException(
                status_code=404,
                detail=f"Job {job_id} not found"
            )
        with open(status_path) as f:
            data = json.load(f)
            job = ProcessingJob(data["job_id"], "")
            job.status = data["status"]
            job.progress = data["progress"]
            job.result_path = data["result_path"]
            job.error = data["error"]
            return job

    async def process(self):
        try:
            self.status = "processing"
            self._save_status()
            logger.info(f"Starting processing job {self.job_id}")

            input_path = os.path.join(settings.UPLOAD_DIR, self.filename)
            if not os.path.exists(input_path):
                raise FileNotFoundError(f"Input file not found: {input_path}")
                
            output_path = os.path.join(
                settings.OUTPUT_DIR,
                f"processed_{self.filename}.txt"
            )

            # Extract text from PDF
            text = self.pdf_service.extract_text_from_pdf(input_path)
            if not text:
                raise Exception("Failed to extract text from PDF")

            # Create chunks and process them
            chunks = self.pdf_service.create_word_bounded_chunks(text)
            processed_chunks = []
            
            # Process chunks with progress tracking
            for i, chunk in enumerate(chunks):
                try:
                    processed_chunk = await self.pdf_service.openai_service.process_chunk(chunk)
                    if processed_chunk:
                        processed_chunks.append(processed_chunk)
                    self.progress = (i + 1) / len(chunks)
                    self._save_status()
                    logger.info(
                        f"Processed chunk {i+1}/{len(chunks)} for job {self.job_id}"
                    )
                except Exception as e:
                    logger.error(f"Error processing chunk {i+1}: {str(e)}")
                    continue

            if not processed_chunks:
                raise Exception("No chunks were successfully processed")

            # Join processed chunks with proper spacing
            processed_text = "\n\n".join(processed_chunks)

            # Save processed text
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(processed_text)

            self.status = "completed"
            self.result_path = output_path
            self._save_status()
            logger.info(f"Completed processing job {self.job_id}")

        except Exception as e:
            logger.error(f"Job {self.job_id} failed: {str(e)}")
            self.status = "failed"
            self.error = str(e)
            self._save_status()
            raise