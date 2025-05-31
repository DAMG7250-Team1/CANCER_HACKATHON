
# import sys
# import os
# import json
# import logging
# from typing import Dict, Any
# from openai import OpenAI
# # from google import genai
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



# from backend.agents.snowflake_agent import SnowflakeAgent
# from backend.agents.rag_agent import get_rag_response
# from backend.agents.web_agent import WebAgent

# logger = logging.getLogger(__name__)

# class CancerResearchMCP:
#     def __init__(self):
#         self.snowflake_agent = SnowflakeAgent()
#         self.web_agent = WebAgent()

#     async def run(self, query: str) -> Dict[str, Any]:
#         try:
#             # Fetch data from each agent
#             snowflake_data = self.snowflake_agent.get_cancer_statistics()
#             rag_summary = await get_rag_response(query)
#             clinical_trials = self.web_agent.get_clinical_trials(query)
#             funding = self.web_agent.get_funding_opportunities(query)
#             hospitals = self.web_agent.get_hospitals_by_location(query)

#             # Format web results
#             clinical_str = "\n\n".join([
#                 f"Title: {item.get('title')}\n"
#                 f"Description: {item.get('description')}\n"
#                 f"Phase: {item.get('phase')}\n"
#                 f"Status: {item.get('status')}\n"
#                 f"Link: {item.get('source_url')}"
#                 for item in clinical_trials
#             ])

#             funding_str = "\n\n".join([
#                 f"Title: {f.get('title')}\n"
#                 f"Description: {f.get('description')}\n"
#                 f"Link: {f.get('source_url')}"
#                 for f in funding
#             ])

#             hospital_str = "\n\n".join([
#                 f"Name: {h.get('name')}\n"
#                 f"Address: {h.get('address')}\n"
#                 f"Rating: {h.get('rating')}\n"
#                 f"Link: {h.get('source_url')}"
#                 for h in hospitals
#             ])

#             # Combine all context
#             snowflake_text = json.dumps(snowflake_data, indent=2)
#             full_context = f"""
#                 === SNOWFLAKE STRUCTURED DATA ===
#                 {snowflake_text}

#                 === RAG RESEARCH SUMMARY ===
#                 {rag_summary}

#                 === CLINICAL TRIALS ===
#                 {clinical_str}

#                 === FUNDING OPPORTUNITIES ===
#                 {funding_str}

#                 === TREATMENT CENTERS ===
#                 {hospital_str}
#                 """

#             # Generate today's date
#             import datetime
#             today = datetime.date.today().isoformat()

#             # Comprehensive prompt
#             prompt = f"""
#                 You are an AI-powered Cancer Research Assistant tasked with producing an exceptionally comprehensive, peer-reviewed style oncology report. Use formal academic English, adopt “we” to describe analyses, and target each main section at 300–500 words. Include numbered lists, detailed figures, and exhaustive bullet summaries.

#                 EXECUTIVE SUMMARY:
#                 - Provide a succinct overview (2–3 paragraphs) of the study’s purpose, key findings, and implications.

#                 TITLE PAGE:
#                 1. Title: Auto-generate a precise, descriptive title reflecting the query.
#                 2. Running head: ≤50 characters.
#                 3. Author: AI Cancer Research Assistant.
#                 4. Affiliation: Cancer Research Platform.
#                 5. Date: {today}.
#                 6. Keywords: List 5–7, comma-separated.
#                 7. Table of Contents: Enumerate sections with page numbers.

#                 ABSTRACT (200–250 words):
#                 - Background, Objectives, Methods, Key Results (with numeric highlights), Conclusions.

#                 INTRODUCTION:
#                 - Contextualize the cancer topic against current literature, cite 3–5 key studies in APA style.
#                 - State research questions or hypotheses.
#                 - Conclude with a concise bullet summary.

#                 METHODS:
#                 1. Data Sources:
#                 a. Snowflake epidemiological dataset (years, populations, event types).
#                 b. RAG-derived literature summaries (inclusion/exclusion criteria).
#                 c. Real-time web data (Tavily clinical trials, funding, hospitals).
#                 2. Data Cleaning & Preprocessing:
#                 - Describe handling of missing values, data type conversions, and stratification by demographics.
#                 3. Statistical Analysis:
#                 - Formulas:
#                     • Incidence rate per 100,000: `(CASECOUNT/POPULATION)×100000`.
#                     • Year-over-year % change: `((Rate_t – Rate_{{t–1}})/Rate_{{t–1}})×100`.
#                 - Mention statistical tests (e.g., chi-square, t-tests) where relevant.
#                 4. Visualization Plan:
#                 - Line charts, bar graphs, geospatial maps, and allocation pie charts.
#                 5. Software & Libraries:
#                 - E.g., Python 3.11, pandas 2.0.1, matplotlib, geopandas, OpenAI gpt-4o-mini.
#                 - End with a detailed 3-bullet summary.

#                 RESULTS:
#                 5.1 Incidence Trends:
#                 - Table 1: Incidence Rates & YOY Changes.
#                 - Figure 1: Trend line chart.
#                 - Narrative analysis with % growth and statistical significance.
#                 - Bullet summary.

#                 5.2 Literature Insights:
#                 - Summarize 3–5 key findings from RAG with in-text citations.
#                 - Bullet summary.

#                 5.3 Clinical Trials Analysis:
#                 - Trends in phases, status, enrollment numbers.
#                 - URLs in APA format.
#                 - Bullet summary.

#                 5.4 Funding Opportunities:
#                 - Detailed list of grants, amounts, eligibility.
#                 - Pie chart breakdown.
#                 - Bullet summary.

#                 5.5 Treatment Centers by Region:
#                 - Top 5 centers with names, addresses, ratings.
#                 - Geospatial map description.
#                 - Bullet summary.

#                 5.6 Treatment Modalities & Medication Overview:
#                 - List standard-of-care regimens by line of therapy.
#                 - Describe mechanism of action, dosing schedules, and key toxicities.
#                 - Bullet summary.

#                 TABLES:
#                 - Table 1   placeholders with captions.

#                 DISCUSSION:
#                 - Compare findings to ≥2 landmark studies (include DOIs).
#                 - Discuss biological/demographic mechanisms.
#                 - Address data limitations (e.g., VARCHAR year fields, missing metrics).
#                 - Propose future RCTs or registry enhancements.
#                 - Bullet summary.

#                 CONCLUSION:
#                 - Synthesize main takeaways.
#                 - Implications for policy/clinical practice.
#                 - Future research directions.
#                 - Bullet summary.

#                 REFERENCES (APA):
#                 - Full APA citations for all sources, with DOIs.

#                 APPENDICES:
#                 - Raw data tables.
#                 - Sample code snippets for analyses.

#                 **User Query:**
#                 {query}

#                 **All Available Data:**
#                 {full_context}
#                 """

         
            
#             from google import genai
            

#             # initialize the client (Gemini Developer API)
#             client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

#             # start a stateful chat session
#             chat = client.chats.create(model="gemini-2.0-flash-001")

#             # send your prompt
#             resp = chat.send_message(prompt)

            
#             # full_report = response.choices[0].message.content
#             full_report = resp.text
#             return {"report": full_report}

#         except Exception as e:
#             logger.exception("Error during full report generation")
#             return {"report": f"Error generating report: {str(e)}"}














# import os
# import json
# import pandas as pd
# import numpy as np
# from typing import Dict, Any, List
# from openai import OpenAI
# from google import genai
# import logging
# import datetime
# import logging

# logger = logging.getLogger(__name__)

# # Import your agent modules here (update paths as needed)
# from backend.agents.snowflake_agent import SnowflakeAgent
# from backend.agents.rag_agent import get_rag_response
# from backend.agents.web_agent import WebAgent

# logger = logging.getLogger(__name__)

# # === Embedding & Summarization Helpers ===

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# EMBED_MODEL = "text-embedding-ada-002"

# def get_embeddings(texts: List[str]) -> np.ndarray:
#     client = OpenAI(api_key=OPENAI_API_KEY)
#     resp = client.embeddings.create(input=texts, model=EMBED_MODEL)
#     return np.array([r.embedding for r in resp.data])

# def cosine_similarity(vecs, query_vec):
#     return np.dot(vecs, query_vec) / (np.linalg.norm(vecs, axis=1) * np.linalg.norm(query_vec) + 1e-10)

# def chunk_text(text, max_words=200):
#     words = text.split()
#     return [' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

# def summarize_text(chat, text, section_label, max_words=500):
#     """Recursive summarization: splits if too long, summarizes each chunk, repeats if needed."""
#     if len(text.split()) < max_words:
#         return text
#     chunks = chunk_text(text, max_words)
#     summaries = []
#     for chunk in chunks:
#         prompt = f"Summarize this {section_label} section for an oncology report:\n{chunk}"
#         summaries.append(chat.send_message(prompt).text)
#     joined = "\n".join(summaries)
#     if len(joined.split()) > max_words:
#         return summarize_text(chat, joined, section_label, max_words)
#     return joined

# def format_top(json_list, keys, label, n=3):
#     return "\n\n".join([
#         "\n".join([f"{k.capitalize()}: {item.get(k, '')}" for k in keys if k in item])
#         for item in json_list[:n]
#     ]) or f"No {label} found."


# # === CancerResearchMCP ===

# class CancerResearchMCP:
#     def __init__(self):
#         self.snowflake_agent = SnowflakeAgent()
#         self.web_agent = WebAgent()

#     async def run(self, query: str) -> Dict[str, Any]:
#         try:
#             # === Fetch Data from Each Agent ===
#             snowflake_data = self.snowflake_agent.get_cancer_statistics()
#             # Convert snowflake_data (likely dict/list of dict) to DataFrame for processing
#             if isinstance(snowflake_data, list):
#                 snowflake_df = pd.DataFrame(snowflake_data)
#             elif isinstance(snowflake_data, dict):
#                 snowflake_df = pd.DataFrame([snowflake_data])
#             else:
#                 snowflake_df = pd.DataFrame()

#             rag_summary = await get_rag_response(query)
#             clinical_trials = self.web_agent.get_clinical_trials(query)
#             funding = self.web_agent.get_funding_opportunities(query)
#             hospitals = self.web_agent.get_hospitals_by_location(query)

#             # === Initialize Gemini Chat ===
#             gemini_key = os.getenv("GEMINI_API_KEY")
#             client = genai.Client(api_key=gemini_key)
#             chat = client.chats.create(model="gemini-2.0-flash-001")

#             # === Build Hybrid Context ===
#             # 1. Snowflake (Tabular)
#             try:
#                 summary = snowflake_df.describe(include="all").to_string()
#                 top_rows = snowflake_df.head(5).to_markdown(index=False)
#                 snowflake_section = f"{summary}\n\nTop rows:\n{top_rows}"
#                 snowflake_short = summarize_text(chat, snowflake_section, "Epidemiology Table")
#             except Exception as e:
#                 snowflake_short = f"Could not process table: {e}"

#             # 2. RAG (Unstructured)
#             rag_chunks = chunk_text(rag_summary, max_words=200)
#             chunk_embeddings = get_embeddings(rag_chunks)
#             query_embedding = get_embeddings([query])[0]
#             sims = cosine_similarity(chunk_embeddings, query_embedding)
#             top_idx = sims.argsort()[::-1][:3]
#             rag_relevant = "\n\n".join([rag_chunks[i] for i in top_idx])
#             rag_short = summarize_text(chat, rag_relevant, "Literature Summary")

#             # 3. Web Agent Data (JSON)
#             clinical_str = format_top(clinical_trials, ["title", "description", "phase", "status", "source_url"], "Clinical Trials")
#             clinical_short = summarize_text(chat, clinical_str, "Clinical Trials")

#             funding_str = format_top(funding, ["title", "description", "source_url"], "Funding")
#             funding_short = summarize_text(chat, funding_str, "Funding")

#             hospital_str = format_top(hospitals, ["name", "address", "rating", "source_url"], "Hospitals")
#             hospital_short = summarize_text(chat, hospital_str, "Hospitals")

#             # === Final Context for Prompt ===
#             context = f"""
#                     === EPIDEMIOLOGY SUMMARY ===
#                     {snowflake_short}

#                     === LITERATURE SUMMARY (RAG) ===
#                     {rag_short}

#                     === CLINICAL TRIALS (Top 3) ===
#                     {clinical_short}

#                     === FUNDING (Top 3) ===
#                     {funding_short}

#                     === HOSPITALS (Top 3) ===
#                     {hospital_short}
#                     """
#             logger.info("\n===== SNOWFLAKE DATA =====\n%s", snowflake_short)
#             logger.info("\n===== RAG DATA =====\n%s", rag_short)
#             logger.info("\n===== CLINICAL TRIALS DATA =====\n%s", clinical_short)
#             logger.info("\n===== FUNDING DATA =====\n%s", funding_short)
#             logger.info("\n===== HOSPITALS DATA =====\n%s", hospital_short)
            
            
#             today = datetime.date.today().isoformat()
#             prompt = f"""
#                     You are an AI-powered Cancer Research Assistant tasked with producing an exceptionally comprehensive, peer-reviewed style oncology report. Use formal academic English, adopt “we” to describe analyses, and target each main section at 300–500 words. Include numbered lists, detailed figures, and exhaustive bullet summaries.

#                     EXECUTIVE SUMMARY:
#                     - Provide a succinct overview (2–3 paragraphs) of the study’s purpose, key findings, and implications.

#                     TITLE PAGE:
#                     1. Title: Auto-generate a precise, descriptive title reflecting the query.
#                     2. Running head: ≤50 characters.
#                     3. Author: AI Cancer Research Assistant.
#                     4. Affiliation: Cancer Research Platform.
#                     5. Date: {today}.
#                     6. Keywords: List 5–7, comma-separated.
#                     7. Table of Contents: Enumerate sections with page numbers.

#                     ABSTRACT (200–250 words):
#                     - Background, Objectives, Methods, Key Results (with numeric highlights), Conclusions.

#                     INTRODUCTION:
#                     - Contextualize the cancer topic against current literature, cite 3–5 key studies in APA style.
#                     - State research questions or hypotheses.
#                     - Conclude with a concise bullet summary.

#                     METHODS:
#                     1. Data Sources:
#                     a. Snowflake epidemiological dataset (years, populations, event types).
#                     b. RAG-derived literature summaries (inclusion/exclusion criteria).
#                     c. Real-time web data (clinical trials, funding, hospitals).
#                     2. Data Cleaning & Preprocessing:
#                     - Describe handling of missing values, data type conversions, and stratification by demographics.
#                     3. Statistical Analysis:
#                     - Formulas:
#                         • Incidence rate per 100,000: `(CASECOUNT/POPULATION)×100000`.
#                         • Year-over-year % change: `((Rate_t – Rate_{{t–1}})/Rate_{{t–1}})×100`.
#                     - Mention statistical tests (e.g., chi-square, t-tests) where relevant.
#                     4. Visualization Plan:
#                     - Line charts, bar graphs, geospatial maps, and allocation pie charts.
#                     5. Software & Libraries:
#                     - E.g., Python 3.11, pandas 2.0.1, matplotlib, geopandas, OpenAI gpt-4o-mini.
#                     - End with a detailed 3-bullet summary.

#                     RESULTS:
#                     5.1 Incidence Trends:
#                     - Table 1: Incidence Rates & YOY Changes.
#                     - Figure 1: Trend line chart.
#                     - Narrative analysis with % growth and statistical significance.
#                     - Bullet summary.

#                     5.2 Literature Insights:
#                     - Summarize 3–5 key findings from RAG with in-text citations.
#                     - Bullet summary.

#                     5.3 Clinical Trials Analysis:
#                     - Trends in phases, status, enrollment numbers.
#                     - URLs in APA format.
#                     - Bullet summary.

#                     5.4 Funding Opportunities:
#                     - Detailed list of grants, amounts, eligibility.
#                     - Pie chart breakdown.
#                     - Bullet summary.

#                     5.5 Treatment Centers by Region:
#                     - Top 5 centers with names, addresses, ratings.
#                     - Geospatial map description.
#                     - Bullet summary.

#                     5.6 Treatment Modalities & Medication Overview:
#                     - List standard-of-care regimens by line of therapy.
#                     - Describe mechanism of action, dosing schedules, and key toxicities.
#                     - Bullet summary.

#                     TABLES:
#                     - Table 1 placeholders with captions.

#                     DISCUSSION:
#                     - Compare findings to ≥2 landmark studies (include DOIs).
#                     - Discuss biological/demographic mechanisms.
#                     - Address data limitations (e.g., VARCHAR year fields, missing metrics).
#                     - Propose future RCTs or registry enhancements.
#                     - Bullet summary.

#                     CONCLUSION:
#                     - Synthesize main takeaways.
#                     - Implications for policy/clinical practice.
#                     - Future research directions.
#                     - Bullet summary.

#                     REFERENCES (APA):
#                     - Full APA citations for all sources, with DOIs.

#                     APPENDICES:
#                     - Raw data tables.
#                     - Sample code snippets for analyses.

#                     **User Query:**
#                     {query}

#                     **All Available Data:**
#                     {context}
#                     """

#             logger.info("Prompt size: %d words", len(prompt.split()))
#             response = chat.send_message(prompt)
#             return {"report": response.text}

#         except Exception as e:
#             logger.exception("Error during full report generation")
#             return {"report": f"Error generating report: {str(e)}"}











import os
import json
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from openai import OpenAI
from google import genai
import logging
import datetime
import time

logger = logging.getLogger(__name__)

from backend.agents.snowflake_agent import SnowflakeAgent
from backend.agents.rag_agent import get_rag_response
from backend.agents.web_agent import WebAgent

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = "text-embedding-ada-002"

def get_embeddings(texts: List[str]) -> np.ndarray:
    client = OpenAI(api_key=OPENAI_API_KEY)
    resp = client.embeddings.create(input=texts, model=EMBED_MODEL)
    return np.array([r.embedding for r in resp.data])

def cosine_similarity(vecs, query_vec):
    return np.dot(vecs, query_vec) / (np.linalg.norm(vecs, axis=1) * np.linalg.norm(query_vec) + 1e-10)

def chunk_text(text, max_words=500):
    words = text.split()
    return [' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

def summarize_text(chat, text, section_label, max_words=1000, max_recursion=1, depth=0):
    """Summarize only if needed, and avoid recursive explosion."""
    if len(text.split()) < max_words or depth >= max_recursion:
        return text
    chunks = chunk_text(text, max_words)
    summaries = []
    for chunk in chunks:
        prompt = f"Summarize this {section_label} section for an oncology report:\n{chunk}"
        while True:
            try:
                summary = chat.send_message(prompt).text
                break
            except Exception as e:
                if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                    logger.warning("Hit Gemini quota/rate limit, sleeping for 60s before retry...")
                    time.sleep(60)
                else:
                    logger.exception(f"Unexpected LLM error: {e}")
                    summary = "Summarization failed."
                    break
        summaries.append(summary)
    joined = "\n".join(summaries)
    if len(joined.split()) > max_words and depth < max_recursion:
        # Only one recursive summarization allowed!
        return summarize_text(chat, joined, section_label, max_words, max_recursion, depth+1)
    return joined

def format_top(json_list, keys, label, n=3):
    return "\n\n".join([
        "\n".join([f"{k.capitalize()}: {item.get(k, '')}" for k in keys if k in item])
        for item in json_list[:n]
    ]) or f"No {label} found."


class CancerResearchMCP:
    def __init__(self):
        self.snowflake_agent = SnowflakeAgent()
        self.web_agent = WebAgent()

    async def run(self, query: str) -> Dict[str, Any]:
        try:
            # === Fetch Data from Each Agent ===
            snowflake_data = self.snowflake_agent.get_cancer_statistics()
            if isinstance(snowflake_data, list):
                snowflake_df = pd.DataFrame(snowflake_data)
            elif isinstance(snowflake_data, dict):
                snowflake_df = pd.DataFrame([snowflake_data])
            else:
                snowflake_df = pd.DataFrame()

            rag_summary = await get_rag_response(query)
            clinical_trials = self.web_agent.get_clinical_trials(query)
            funding = self.web_agent.get_funding_opportunities(query)
            hospitals = self.web_agent.get_hospitals_by_location(query)

            gemini_key = os.getenv("GEMINI_API_KEY")
            client = genai.Client(api_key=gemini_key)
            chat = client.chats.create(model="gemini-2.0-flash-001")

            # === Build Hybrid Context with Reduced Gemini Usage ===

            # 1. Snowflake (Tabular)
            try:
                summary = snowflake_df.describe(include="all").to_string()
                try:
                    top_rows = snowflake_df.head(5).to_markdown(index=False)
                except ImportError:
                    top_rows = snowflake_df.head(5).to_string(index=False)
                snowflake_section = f"{summary}\n\nTop rows:\n{top_rows}"
                # Only summarize if very large!
                snowflake_short = summarize_text(chat, snowflake_section, "Epidemiology Table", max_words=1000)
            except Exception as e:
                snowflake_short = f"Could not process table: {e}"

            # 2. RAG (Unstructured)
            rag_chunks = chunk_text(rag_summary, max_words=500)
            chunk_embeddings = get_embeddings(rag_chunks)
            query_embedding = get_embeddings([query])[0]
            sims = cosine_similarity(chunk_embeddings, query_embedding)
            top_idx = sims.argsort()[::-1][:3]
            rag_relevant = "\n\n".join([rag_chunks[i] for i in top_idx])
            rag_short = summarize_text(chat, rag_relevant, "Literature Summary", max_words=1000)

            # 3. Web Agent Data (JSON)
            clinical_str = format_top(clinical_trials, ["title", "description", "phase", "status", "source_url"], "Clinical Trials")
            clinical_short = summarize_text(chat, clinical_str, "Clinical Trials", max_words=1000)

            funding_str = format_top(funding, ["title", "description", "source_url"], "Funding")
            funding_short = summarize_text(chat, funding_str, "Funding", max_words=1000)

            hospital_str = format_top(hospitals, ["name", "address", "rating", "source_url"], "Hospitals")
            hospital_short = summarize_text(chat, hospital_str, "Hospitals", max_words=1000)

            context = f"""
=== EPIDEMIOLOGY SUMMARY ===
{snowflake_short}

=== LITERATURE SUMMARY (RAG) ===
{rag_short}

=== CLINICAL TRIALS (Top 3) ===
{clinical_short}

=== FUNDING (Top 3) ===
{funding_short}

=== HOSPITALS (Top 3) ===
{hospital_short}
"""

            logger.info("\n===== SNOWFLAKE DATA =====\n%s", snowflake_short)
            # logger.info("\n===== RAG DATA =====\n%s", rag_short)
            # logger.info("\n===== CLINICAL TRIALS DATA =====\n%s", clinical_short)
            # logger.info("\n===== FUNDING DATA =====\n%s", funding_short)
            # logger.info("\n===== HOSPITALS DATA =====\n%s", hospital_short)

            today = datetime.date.today().isoformat()
            prompt = f"""
You are an AI-powered Cancer Research Assistant tasked with producing an exceptionally comprehensive, peer-reviewed style oncology report. Use Markdown headings and tables. Use formal academic English, adopt “we” to describe analyses, and target each main section at 300–500 words. Include numbered lists, detailed figures, and exhaustive bullet summaries. For each Results section, cite numeric values and sources directly from the context below.

EXECUTIVE SUMMARY:
- Provide a succinct overview (2–3 paragraphs) of the study’s purpose, key findings, and implications.

TITLE PAGE:
1. Title: Auto-generate a precise, descriptive title reflecting the query.
2. Running head: ≤50 characters.
3. Author: AI Cancer Research Assistant.
4. Affiliation: Cancer Research Platform.
5. Date: {today}.
6. Keywords: List 5–7, comma-separated.
7. Table of Contents: Enumerate sections with page numbers.

ABSTRACT (200–250 words):
- Background, Objectives, Methods, Key Results (with numeric highlights), Conclusions.

INTRODUCTION:
- Contextualize the cancer topic against current literature, cite 3–5 key studies in APA style.
- State research questions or hypotheses.
- Conclude with a concise bullet summary.

METHODS:
1. Data Sources:
a. Snowflake epidemiological dataset (years, populations, event types).
b. RAG-derived literature summaries (inclusion/exclusion criteria).
c. Real-time web data (clinical trials, funding, hospitals).
2. Data Cleaning & Preprocessing:
- Describe handling of missing values, data type conversions, and stratification by demographics.
3. Statistical Analysis:
- Formulas:
    • Incidence rate per 100,000: `(CASECOUNT/POPULATION)×100000`.
    • Year-over-year % change: `((Rate_t – Rate_{{t–1}})/Rate_{{t–1}})×100`.
- Mention statistical tests (e.g., chi-square, t-tests) where relevant.
4. Visualization Plan:
- Line charts, bar graphs, geospatial maps, and allocation pie charts.
5. Software & Libraries:
- E.g., Python 3.11, pandas 2.0.1, matplotlib, geopandas, OpenAI gpt-4o-mini.
- End with a detailed 3-bullet summary.

RESULTS:
5.1 Incidence Trends:
- Table 1: Incidence Rates & YOY Changes.
- Figure 1: Trend line chart.
- Narrative analysis with % growth and statistical significance.
- Bullet summary.

5.2 Literature Insights:
- Summarize 3–5 key findings from RAG with in-text citations.
- Bullet summary.

5.3 Clinical Trials Analysis:
- Trends in phases, status, enrollment numbers.
- URLs in APA format.
- Bullet summary.

5.4 Funding Opportunities:
- Detailed list of grants, amounts, eligibility.
- Pie chart breakdown.
- Bullet summary.

5.5 Treatment Centers by Region:
- Top 5 centers with names, addresses, ratings.
- Geospatial map description.
- Bullet summary.

5.6 Treatment Modalities & Medication Overview:
- List standard-of-care regimens by line of therapy.
- Describe mechanism of action, dosing schedules, and key toxicities.
- Bullet summary.

TABLES:
- Table 1 placeholders with captions.

DISCUSSION:
- Compare findings to ≥2 landmark studies (include DOIs).
- Discuss biological/demographic mechanisms.
- Address data limitations (e.g., VARCHAR year fields, missing metrics).
- Propose future RCTs or registry enhancements.
- Bullet summary.

CONCLUSION:
- Synthesize main takeaways.
- Implications for policy/clinical practice.
- Future research directions.
- Bullet summary.

REFERENCES (APA):
- Full APA citations for all sources, with DOIs.

APPENDICES:
- Raw data tables.
- Sample code snippets for analyses.

**User Query:**
{query}

**All Available Data:**
{context}
"""

            logger.info("Prompt size: %d words", len(prompt.split()))
            try:
                response = chat.send_message(prompt)
            except Exception as e:
                if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                    logger.warning("Gemini API quota exceeded or rate limit hit. Ask user to try again later.")
                    return {"report": "Gemini API quota exceeded, please wait and try again in a minute."}
                logger.exception("LLM call failed")
                return {"report": f"Error generating report: {str(e)}"}

            return {"report": response.text}

        except Exception as e:
            logger.exception("Error during full report generation")
            return {"report": f"Error generating report: {str(e)}"}
