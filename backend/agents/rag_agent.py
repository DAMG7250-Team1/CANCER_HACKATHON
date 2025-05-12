import os
import logging
import time
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from core.s3_client import S3FileManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_environment():
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
    load_dotenv(dotenv_path)

    required_vars = ["AWS_BUCKET_NAME", "OPENAI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")

    return {
        "aws_bucket": os.getenv("AWS_BUCKET_NAME"),
        "openai_api_key": os.getenv("OPENAI_API_KEY")
    }

class RAGAgent:
    def __init__(self):
        self.config = load_environment()
        self.openai_client = OpenAI(api_key=self.config['openai_api_key'])
        self.s3_client = S3FileManager(self.config['aws_bucket'])

    async def fetch_documents_from_s3(self, query: str) -> List[str]:
        logger.info(f"Fetching documents for query: {query}")
        files = self.s3_client.list_files()
        if not files:
            logger.warning("No files found in S3")
            return []

        # Only pick PDFs
        pdf_files = [f for f in files if f.endswith(".pdf")]

        # Extract cancer type
        detected_cancer = next((ct for ct in ["brain", "blood", "skin", "lung", "breast"] if ct in query.lower()), None)
        
        # Filter for relevant ones or fallback to first 3
        relevant_files = [f for f in pdf_files if detected_cancer and detected_cancer in f.lower()]
        if not relevant_files:
            logger.warning("No cancer-type specific files found, using fallback")
            relevant_files = pdf_files

        documents = []
        for file in relevant_files[:3]:  # limit to top 3
            try:
                from features.mistral_parser import pdf_mistralocr_converter
                pdf_content = self.s3_client.load_s3_pdf(file)
                _, markdown = pdf_mistralocr_converter(pdf_content, "research-papers", self.s3_client)
                documents.append(markdown)
            except Exception as e:
                logger.exception(f"Error processing PDF {file}")

        logger.info(f"Returning {len(documents)} documents for query")
        return documents

    async def generate_response(self, query: str, documents: List[str]) -> str:
        logger.info(f"Generating response from {len(documents)} documents")
        if not documents:
            return "No relevant information available."

        context = "\n---\n".join(documents)
        prompt = f"""
        You are a cancer research assistant.
        Answer the question: {query}
        Based on the following context:
        {context}
        """

        start = time.time()
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800
        )
        logger.info(f"OpenAI response took {time.time() - start:.2f}s")

        return response.choices[0].message.content

async def get_rag_response(query: str) -> str:
    agent = RAGAgent()
    documents = await agent.fetch_documents_from_s3(query)
    if not documents:
        return "No documents found for the query."
    return await agent.generate_response(query, documents)





