# === app.py ===
import streamlit as st
import requests
from io import BytesIO
from xhtml2pdf import pisa

st.set_page_config(page_title="Cancer Research Dashboard", page_icon="🔬", layout="wide")
BACKEND_URL = "http://localhost:8000"

st.title("🔬 Cancer Research Dashboard")
st.markdown("""
This dashboard provides AI-generated cancer research reports based on:
- 📊 Statistical data (Snowflake)
- 📚 Literature (RAG from S3)
- 🌐 Web search (Tavily clinical trials)
""")

with st.sidebar:
    st.header("Research Parameters")
    query = st.text_area("Research Query", placeholder="Enter your question... e.g., cancer trends for children 2000")


def generate_pdf(html_text: str) -> bytes:
    pdf_buffer = BytesIO()
    pisa.CreatePDF(html_text, dest=pdf_buffer)
    return pdf_buffer.getvalue()

if st.sidebar.button("Generate Comprehensive Research Report"):
    if not query:
        st.error("Please enter a research query.")
    else:
        st.info("Sending query to backend...")
        try:
            response = requests.post(f"{BACKEND_URL}/generate_report", json={"query": query}, timeout=120)
            response.raise_for_status()
            data = response.json()

            report_text = data.get("report", "")
            if report_text:
                st.header("📌 Comprehensive Cancer Research Report")
                st.markdown(report_text)

                summary_html = f"""
                <h1>Cancer Research Report</h1>
                <h2>Query: {query}</h2>
                <p>{report_text.replace('\n', '<br>')}</p>
                """

                pdf_bytes = generate_pdf(summary_html)

                st.download_button(
                    label="📅 Download Full Report (PDF)",
                    data=pdf_bytes,
                    file_name="cancer_research_report.pdf",
                    mime="application/pdf"
                )
            else:
                st.warning("No report was generated.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown("---")
st.markdown("Cancer Research Assistant | Powered by OpenAI + Multi-Agent System")
