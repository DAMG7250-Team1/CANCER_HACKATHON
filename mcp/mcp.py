

import sys
import os
import json
import logging
import time
from typing import Dict, Any, List, Tuple
from datetime import date

# make sure project packages are on the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agents.snowflake_agent import SnowflakeAgent
from backend.agents.rag_agent import get_rag_response
from backend.agents.web_agent import WebAgent

from google import genai
from google.genai import errors

# ── Logging ─────────────────────────────────────────
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ── Configuration ───────────────────────────────────
MODEL_NAME          = "gemini-2.0-flash-001"
COMPRESSION_BUDGET  = 400
SECTIONS: List[Tuple[str,int]] = [
    ("EXECUTIVE SUMMARY",  800),
    ("TITLE & ABSTRACT",   600),
    ("INTRODUCTION",       800),
    ("METHODS",            600),
    ("RESULTS",           1200),
    ("DISCUSSION",         800),
    ("CONCLUSION",         400),
]

# ── Helpers ─────────────────────────────────────────
def with_backoff(fn, retries: int = 3, base_delay: float = 2.0):
    """Retry on 429 errors with exponential backoff."""
    for i in range(retries):
        try:
            return fn()
        except errors.ClientError as e:
            if e.status_code == 429:
                delay = base_delay * (2 ** i)
                logger.warning(f"Rate limit hit, retrying in {delay:.1f}s…")
                time.sleep(delay)
            else:
                raise
    # final attempt
    return fn()

def compress_segment(client: genai.Client, label: str, text: str, max_tokens: int = COMPRESSION_BUDGET) -> str:
    """Ask Gemini to summarize a chunk into ≤ max_tokens."""
    chat = client.chats.create(model=MODEL_NAME)
    prompt = f"Summarize this {label} into no more than {max_tokens} tokens:\n\n{text}"
    resp = with_backoff(lambda: chat.send_message(prompt))
    return resp.last.content.strip()

def generate_section(client: genai.Client, context: str, name: str, max_tokens: int) -> str:
    """Generate one section of the report given the lean context."""
    chat = client.chats.create(model=MODEL_NAME, temperature=0.7)
    prompt = (
        "You are an AI-powered Cancer Research Assistant writing for a peer-reviewed oncology journal. "
        "Use formal academic English and adopt “we” when describing analyses.\n\n"
        f"Based on the context below, draft the **{name}** section (~{max_tokens} tokens):\n\n"
        f"---\n{context}\n---\n"
        f"## {name}:\n"
    )
    resp = with_backoff(lambda: chat.send_message(prompt))
    return resp.last.content.strip()

# ── Main Class ───────────────────────────────────────
class CancerResearchMCP:
    def __init__(self):
        self.snowflake_agent = SnowflakeAgent()
        self.web_agent       = WebAgent()
        self.client          = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    async def run(self, query: str) -> Dict[str, Any]:
        try:
            # 1) Fetch raw data
            snowflake_data   = self.snowflake_agent.get_cancer_statistics()
            rag_summary      = await get_rag_response(query)
            clinical_trials  = self.web_agent.get_clinical_trials(query)
            funding_opps     = self.web_agent.get_funding_opportunities(query)
            hospitals        = self.web_agent.get_hospitals_by_location(query)

            # 2) Render each to text
            snowflake_text = json.dumps(snowflake_data, indent=2)
            rag_text       = rag_summary
            trials_text    = "\n\n".join(f"{t['title']}: {t['description']}" for t in clinical_trials)
            funding_text   = "\n\n".join(f"{f['title']}: {f['description']}" for f in funding_opps)
            hosp_text      = "\n\n".join(f"{h['name']}, {h['address']}" for h in hospitals)

            # 3) Compress each chunk into ~400 tokens
            sf_sum   = compress_segment(self.client, "Snowflake data",        snowflake_text)
            rag_sum  = compress_segment(self.client, "RAG literature",        rag_text)
            ct_sum   = compress_segment(self.client, "Clinical trials",       trials_text)
            fd_sum   = compress_segment(self.client, "Funding opportunities", funding_text)
            hs_sum   = compress_segment(self.client, "Hospital information",  hosp_text)

            # 4) Build lean context
            lean_context = "\n\n".join([sf_sum, rag_sum, ct_sum, fd_sum, hs_sum])

            # 5) Generate each section separately
            report_parts: List[str] = []
            for name, budget in SECTIONS:
                section_text = generate_section(self.client, lean_context, name, budget)
                report_parts.append(f"### {name}\n\n{section_text}")

            # 6) Combine
            full_report = "\n\n".join(report_parts)
            return {"report": full_report}

        except Exception as e:
            logger.exception("Error during full report generation")
            return {"report": f"Error generating report: {str(e)}"}
