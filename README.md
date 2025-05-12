
# 🔬 Cancer Research Report Generator

This is a multi-agent AI-powered research assistant that generates comprehensive cancer reports using:

- 📊 **Cancer statistics** from Snowflake
- 📚 **Literature summary** via RAG using OpenAI + PDFs in S3
- 🌐 **Real-time clinical data** via Tavily Web Search

---

## 🧠 System Architecture

```mermaid
graph TD
    A[User Inputs Query via Streamlit UI] --> B[FastAPI Backend - /generate_report]
    B --> C[Multi-Agent MCP Controller]

    C --> D[Snowflake Agent - Cancer Statistics]
    C --> E[RAG Agent - Research Literature from S3 + OpenAI]
    C --> F[Web Agent - Clinical Trials from Tavily]

    D --> G[Returns Structured Stats]
    E --> H[Returns RAG Summary]
    F --> I[Returns Clinical Trials (Markdown)]

    G --> J[API Aggregates]
    H --> J
    I --> J

    J --> K[Streamlit UI Displays & Plots Data]
    K --> L[Downloadable PDF Report]
```

---

## 🔄 System Flow

This system follows a **multi-agent pipeline architecture** for generating cancer research reports based on user queries.

### Step-by-Step Flow:

1. ### 🧑‍💻 User Input via Streamlit (`app.py`)
   - Users interact with a simple UI to enter their **research query**.
   - Upon clicking “Generate Report”, the query is sent to the FastAPI backend:
     ```http
     POST /generate_report { "query": "..." }
     ```

2. ### 🚀 FastAPI Orchestrator (`main.py`)
   - Handles incoming requests and invokes the `CancerResearchMCP` controller to coordinate multiple agents.

3. ### 🧠 MCP (Model Contextual Protocol) Controller (`mcp.py`)
   - Coordinates three domain-specific agents:

     - 🔹 **Snowflake Agent**  
       Queries cancer statistics from Snowflake tables (`by_site`, `incident`, `mortality`, `child_cases`).
     
     - 🔹 **RAG Agent**  
       Downloads relevant cancer PDFs from S3 → converts to Markdown via `mistral_parser.py` → summarizes via OpenAI GPT-4o-mini.

     - 🔹 **Web Agent**  
       Uses Tavily to fetch live clinical trials related to the query (title, phase, status, source).

4. ### 📦 Data Aggregation
   - MCP compiles the outputs:
     ```json
     {
       "snowflake_data": {...},
       "rag_data": { "summary": "..." },
       "web_data": "<clinical trials in markdown>"
     }
     ```

5. ### 📊 Frontend Visualization
   - Streamlit renders:
     - **Dataframes** and **charts** from Snowflake data
     - **Research summaries** and **clinical trials**
     - PDF report generated using XHTML2PDF

---

## 📁 Project Structure

```
├── app.py                     # Streamlit UI
├── main.py                    # FastAPI app (entrypoint)
├── mcp.py                     # MCP orchestrator for all agents
├── agents/
│   ├── snowflake_agent.py     # Structured cancer data from Snowflake
│   ├── rag_agent.py           # S3 document loader + OpenAI summarization
│   ├── web_agent.py           # Tavily clinical trial + literature search
├── core/
│   └── s3_client.py           # AWS S3 PDF manager
├── features/
│   ├── mistral_parser.py      # PDF to Markdown converter
│   └── chunking_stratergy.py  # (Optional) Markdown chunker
├── requirements.txt
├── .env
```

---

## 🚀 Getting Started

### 1. Setup Environment

```bash
python -m venv env
source env/bin/activate  # or .\env\Scripts\activate on Windows

pip install -r requirements.txt
```

### 2. .env Configuration

```
# Snowflake
SNOWFLAKE_ACCOUNT=xyz-region
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_pass
SNOWFLAKE_DATABASE=your_db
SNOWFLAKE_WAREHOUSE=your_wh
SNOWFLAKE_SCHEMA=cdc

# AWS
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_BUCKET_NAME=your-bucket
AWS_REGION=us-east-1

# OpenAI
OPENAI_API_KEY=sk-...

# Tavily
TAVILY_API_KEY=...
```

### 3. Run Services

```bash
# Start backend
uvicorn main:app --reload --port 8000

# Launch frontend
streamlit run app.py
```

---

## 🧪 Example Query

Try: **“What were child lung cancer trends in 2010?”**

---

## 🛠 Tech Stack

| Layer         | Tools                                    |
|---------------|-------------------------------------------|
| Frontend UI   | Streamlit, Plotly                         |
| Backend API   | FastAPI, Uvicorn                          |
| Agents        | OpenAI (RAG), Snowflake, Tavily, S3       |
| PDF Handling  | XHTML2PDF, PyMuPDF                        |
