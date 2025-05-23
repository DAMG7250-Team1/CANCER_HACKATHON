







import os
import io
import re
import base64
import requests
import markdown2
from xhtml2pdf import pisa
import streamlit as st
from requests.exceptions import Timeout, RequestException

# --- Configuration ---

def get_backend_url():
    """Retrieve backend URL from Streamlit secrets or environment variable."""
    try:
        return st.secrets["backend_url"]
    except Exception:
        return os.getenv("BACKEND_URL", "http://localhost:8000")

# BACKEND_URL = get_backend_url()
BACKEND_URL = "http://34.67.158.206"

# --- Core Functions ---

def generate_report(query: str) -> str:
    """Call the backend to generate the markdown report."""
    response = requests.post(
        f"{BACKEND_URL}/generate_report",
        json={"query": query},
        timeout=300
    )
    response.raise_for_status()
    data = response.json()
    return data.get("report", "")


def convert_md_to_html(report_md: str) -> str:
    """Convert Markdown to HTML with styling, embed images."""
    # Convert Markdown to HTML with link auto-detection
    html_body = markdown2.markdown(
        report_md,
        extras=["tables", "fenced-code-blocks", "linkify"]
    )
    # CSS styling for PDF and display
    html_template = f"""
    <html>
      <head>
        <meta charset="utf-8">
        <style>
          body {{ font-family: serif; font-size: 13pt; line-height:1.4; }}
          h1 {{ font-size: 24pt; margin-bottom: 0.5em; }}
          h2 {{ font-size: 18pt; margin-top:1em; margin-bottom:0.4em; }}
          h3 {{ font-size: 14pt; margin-top:0.8em; }}
          table {{ width: 100%; border-collapse: collapse; margin:1em 0; }}
          th, td {{ border: 1px solid #666; padding: 8px; word-wrap: break-word; }}
          th {{ background: #eee; }}
          img {{ max-width: 100%; height: auto; margin: 1em 0; }}
          a {{ color: blue; text-decoration: underline; }}
        </style>
      </head>
      <body>
        {html_body}
      
    """
    return embed_images(html_template)


def embed_images(html: str) -> str:
    """Fetch remote images and embed them as base64 data URIs."""
    def repl(match):
        url = match.group(1)
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                ext = url.split(".")[-1].split("?")[0].lower()
                mime = 'image/png' if ext == 'png' else 'image/jpeg'
                data = base64.b64encode(resp.content).decode('utf-8')
                return f'<img src="data:{mime};base64,{data}"'
        except Exception:
            pass
        return match.group(0)
    return re.sub(r'<img src="([^\"]+)"', repl, html)


def convert_html_to_pdf(html: str) -> bytes | None:
    """Convert HTML string to PDF bytes using xhtml2pdf."""
    out = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(html), dest=out)
    if pisa_status.err:
        return None
    return out.getvalue()

# --- Streamlit Interface ---

st.set_page_config(page_title="Cancer Research Report", layout="wide")

st.title("📝 Cancer Research Report Generator")
query = st.text_input("Enter your research query:")

if st.button("Generate Report"):
    if not query:
        st.error("Please enter a query before generating the report.")
    else:
        with st.spinner("Generating report, please wait…"):
            try:
                report_md = generate_report(query)
                if not report_md:
                    st.warning("No report content returned from backend.")
                else:
                    html_report = convert_md_to_html(report_md)
                    # Display HTML with images and links
                    st.markdown(html_report, unsafe_allow_html=True)

                    # PDF Download
                    pdf_data = convert_html_to_pdf(html_report)
                    if pdf_data:
                        st.download_button(
                            label="⬇️ Download Report as PDF",
                            data=pdf_data,
                            file_name="cancer_research_report.pdf",
                            mime="application/pdf"
                        )
                    else:
                        st.error("PDF generation failed.")
            except Timeout:
                st.error("The request to the backend timed out. Try again later.")
            except RequestException as e:
                st.error(f"Request to backend failed: {e}")
