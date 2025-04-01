Hackathon by

1.Husain

2.Sahil Kasliwal

3.Dhrumil Patel


Application-Streamlit : https://content-extraction-tool-hh9cxuyufdcnur47bpteae.streamlit.app/

Backend API-Google Cloud: https://content-extraction-api-607698884796.us-central1.run.app/docs

Google Codelab: https://codelabs-preview.appspot.com/?file_id=1bhb4Ao13vP9LmXGrna4FjiTFQRoALbYzsEr-Q4W_1Wg#0


🧠 AI-Driven Cancer Research Assistant
This project reimagines our multi-agent AI framework—originally built for real-time financial analysis—as a powerful research assistant for cancer diagnosis, treatment cost analysis, and policy insights.
Developed as part of a hackathon, this system leverages structured, unstructured, and real-time data through orchestrated agents to empower patients, researchers, and policymakers.
🌐 System Architecture
🔁 Multi-Agent Orchestration with LangGraph
We use a multi-agent architecture to break down responsibilities into three specialized agents:
pgsqlCopyEdit           +-----------------+               +------------------+           | Web Search Agent|               |  Snowflake Agent |           |-----------------|               |------------------|           | - Hospital data |               | - Structured data|           | - Treatment cost|               | - Stats & Trends |           +-----------------+               +------------------+                    \                              /                     \                            /                      \                          /                       \                        /                        \                      /                     +-----------------------------+                     |         LangGraph           |                     |     Multi-Agent Orchestrator|                     +-----------------------------+                                |                                |                      +------------------+                      |   RAG Agent      |                      | (Pinecone + RAG) |                      | - Research Papers|                      | - Treatment Efficacy |                      +------------------+                                |                                v                      +------------------+                      |    Streamlit UI  |                      |   + FastAPI API  |                      +------------------+                                |                                v                      +------------------+                      |    Final Report  |                      |  (PDF/HTML/Text) |                      +------------------+ 
📊 Data Sources
Structured Data (Snowflake)
Cancer Incidence & Survival Rates
Mortality Rates by Region
Treatment Costs by Institution
Sources: SEER, hospitals, CDC
Unstructured Data (RAG + Pinecone)
Research Papers on Treatments
Trends in Methodology & Efficacy
Sources: PubMed, Scientific Journals, Hospital Reports
Real-Time Data (Web Agents)
Hospital Availability of Treatments
Live Cost Fluctuations
Funding & Insurance Programs
Sources: Hospital Websites, News, Government Portals
🧠 Agent Responsibilities
Agent	Role
Snowflake Agent	Query and visualize cancer stats, costs, regional trends
RAG Agent	Retrieve papers, summarize efficacy, compare treatment performance
Web Agent	Scrape real-time hospital data, treatment costs, and funding options
📝 Report Generation
The system auto-generates a 15-page research report with the following sections:
Introduction to Cancer Statistics
Global & U.S. Incidence Rates
Survival Rates by Type
Top Hospitals for Treatment
Cost of Treatments
Insurance/Funding Options
Comparing Treatment Efficacy
Latest Research Insights
Real-Time Hospital Data
Regional Survival Trends
Accessibility Challenges
Role of AI in Cancer Treatment
Future Tech & Emerging Research
Policy Recommendations
Final Insights for Stakeholders
🖥️ UI Features
Built using Streamlit + FastAPI, the UI enables:
Searching by cancer type, region, hospital
Real-time treatment cost comparison
Research paper summaries
Funding/insurance info
Visual dashboards & PDF export
🚀 Deployment
Containerized with Docker
Cloud-ready for AWS/GCP
Web agents run in live-update mode
Easily scalable for new disease domains



## Features
- **Multi-Agent System**: Utilizes specialized agents for different tasks:
  - RAG Agent: For retrieval-augmented generation
  - Snowflake Agent: For database interactions
  - Web Agent: For real-time web data collection

- **Advanced Analytics**:
  - Comprehensive data analysis
  - Interactive visualizations
  - Statistical modeling
  - Trend analysis

- **Report Generation**:
  - Detailed PDF reports
  - Data visualizations
  - Source citations
  - Key metrics and insights

## Installation

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Setup
1. Clone the repository:
```bash
git clone https://github.com/DAMG7250-Team1/CACNER_HACKATHON.git
cd nvidia-research-assistant
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory and add the following:
```env
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema

OPENAI_API_KEY=your_openai_api_key
```

## Usage

1. Start the backend server:
```bash
cd backend
python main.py
```

2. Launch the Streamlit frontend:
```bash
cd frontend
streamlit run app.py
```

3. Access the application 

## Technologies Used
- **Backend**:
  - Python
  - LangGraph
  - OpenAI
  - Snowflake
  - pandas
  - NumPy

- **Frontend**:
  - Streamlit
  - Plotly
  - ReportLab

- **Data Storage**:
  - Snowflake
  - Vector Stores

## Development
- Follow PEP 8 style guide
- Use type hints
- Write unit tests for new features
- Document code changes

## Testing
Run tests using:
```bash
python -m pytest backend/test_pipeline.py
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Team
- DAMG7250 Team 1
- Northeastern University

## Acknowledgments
- NVIDIA
- OpenAI
- Snowflake
# 

Photos:
![Dashboard](assets/1.png)
![Dashboard](assets/2.png)
![Dashboard](assets/3.png)
![Dashboard](assets/4.png)
![Dashboard](assets/5.png)
![Dashboard](assets/6.png)
![Dashboard](assets/7.png)
![Dashboard](assets/8.png)
![Dashboard](assets/9.png)



Contributions are 33% from all team memebers.