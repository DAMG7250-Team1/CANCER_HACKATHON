# 🔬 Cancer Research Assistant

A multi-agent AI-powered system for generating comprehensive cancer research reports.  
It combines structured cancer statistics (Snowflake), research literature (RAG from S3), and real-time clinical trial data (Tavily API) — summarized by OpenAI GPT.

---

## 🚀 Features

- 📈 **Snowflake Agent**: Pulls structured cancer data (e.g., by site, year, population)
- 📚 **RAG Agent**: Fetches & summarizes PDF research from S3 using OpenAI
- 🌐 **Web Agent**: Scrapes real-time clinical trial info via Tavily
- 🧠 **MCP**: Orchestrates all agents and routes data to OpenAI for final report
- 🖥️ **Frontend**: Streamlit dashboard to visualize results and download PDF

---

## 🧠 Architecture Overview

```
User Query → Streamlit UI
            ↓
        FastAPI Backend
            ↓
     CancerResearchMCP (Coordinator)
       ├── SnowflakeAgent → stats
       ├── RAGAgent → S3 → Markdown → OpenAI
       └── WebAgent → Tavily API
            ↓
  All data passed to OpenAI → GPT-4o → Final Report
            ↓
  Streamlit UI ← Full report + PDF download
```

---

## ⚙️ Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file:

```env
# Snowflake
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_pass
SNOWFLAKE_WAREHOUSE=your_wh
SNOWFLAKE_DATABASE=your_db
SNOWFLAKE_SCHEMA=cdc

# AWS S3
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
AWS_BUCKET_NAME=your-bucket-name

# OpenAI
OPENAI_API_KEY=your_openai_key

# Tavily
TAVILY_API_KEY=your_tavily_key
```

### 3. Run Backend (FastAPI)

```bash
uvicorn main:app --reload
```

### 4. Run Frontend (Streamlit)

```bash
streamlit run app.py
```

---

## 📂 Project Structure

```
├── app.py               # Streamlit frontend
├── main.py              # FastAPI backend
├── mcp/                 # Multi-agent orchestrator
│   └── mcp.py
├── backend/agents/      # Sub-agents
│   ├── snowflake_agent.py
│   ├── rag_agent.py
│   └── web_agent.py
├── core/
│   └── s3_client.py
├── features/
    ├── mistral_parser.py
    └── chunking_stratergy.py
```

---

## 📄 Output

- ✅ Streamlit displays the AI-generated report
- ✅ Option to download a nicely formatted **PDF**
- ✅ Works with all cancer-related queries (e.g., “brain cancer in children in 2010”)

---

## 🤝 Credits

Built for [NEU DAMG Hackathon 2025].  
Uses: Snowflake, AWS S3, OpenAI, Tavily, Streamlit, FastAPI.

---

## 🤪 Sample Query

```
What are the trends in child brain cancer from 2000–2020?
```

Will fetch:
- Snowflake statistics
- S3 research papers
- Clinical trial updates
And generate a unified report with graphs, markdown, and downloadable PDF.


##  Outcome

```
using GPT - https://github.com/DAMG7250-Team1/CANCER_HACKATHON/blob/main/cancer_research_report%20using%20GPT%20model.pdf

and Gemini - 
```
