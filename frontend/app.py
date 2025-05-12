
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import pdfkit
import tempfile
import os
from xhtml2pdf import pisa
from io import BytesIO


st.set_page_config(page_title="Cancer Research Dashboard", page_icon="🔬", layout="wide")

BACKEND_URL = "http://localhost:8000"

st.title("🔬 Cancer Research Dashboard")
st.markdown("""
This dashboard provides comprehensive cancer research analysis combining:
- 📊 Statistical data (from Snowflake)
- 📚 Research literature (via RAG + OpenAI)
- 🌐 Web search (Tavily clinical trials, treatment, etc.)
""")

with st.sidebar:
    st.header("Research Parameters")
    query = st.text_area(
        "Research Query",
        placeholder="Enter your research question...\nExample: 'What were the cancer statistics in 2000 for children?'",
    )


def generate_pdf(summary_html: str) -> bytes:
    pdf_buffer = BytesIO()
    pisa_status = pisa.CreatePDF(summary_html, dest=pdf_buffer)

    if pisa_status.err:
        raise RuntimeError("PDF generation failed with xhtml2pdf")

    return pdf_buffer.getvalue()

    # pdf_file_path = tmp_html_path.replace(".html", ".pdf")
    # pdfkit.from_file(tmp_html_path, pdf_file_path)

    # with open(pdf_file_path, "rb") as f:
    #     pdf_content = f.read()

    # os.remove(tmp_html_path)
    # os.remove(pdf_file_path)
    # return pdf_content

def show_table(title, dataset):
    if dataset:
        df = pd.DataFrame(dataset)
        st.subheader(f"📄 {title}")
        st.dataframe(df)
    else:
        # st.info(f"No data found for **{title}**")
        pass
def extract_start_year(val):
    try:
        return int(str(val).split("-")[0])
    except:
        return None

if st.sidebar.button("Generate Comprehensive Research Report"):
    if not query:
        st.error("Please enter a research query.")
    else:
        progress_placeholder = st.empty()
        progress_bar = st.progress(0)

        progress_placeholder.write("Sending query to backend...")
        progress_bar.progress(30)

        try:
            response = requests.post(
                f"{BACKEND_URL}/generate_report",
                json={"query": query},
                timeout=120
            )
            response.raise_for_status()
            data = response.json()

            progress_placeholder.write("Processing response...")
            progress_bar.progress(70)

            progress_placeholder.empty()
            progress_bar.progress(100)
            st.success("Report generated successfully!")

            st.header("📌 Introduction & Key Findings")
            st.markdown(f"This report is based on your query: **{query}**")

            # --- Snowflake data ---
            st.header("📊 Global Cancer Statistics")
            snowflake_data = data.get("snowflake_data", {})
            show_table("By Site", snowflake_data.get("by_site", []))
            show_table("Incidence", snowflake_data.get("incident", []))
            show_table("Mortality", snowflake_data.get("mortality", []))
            show_table("Child Cases", snowflake_data.get("child_cases", []))

            child_cases = snowflake_data.get("child_cases", [])
            if child_cases:
                df_child = pd.DataFrame(child_cases)
                df_child["YEAR"] = df_child["YEAR"].apply(extract_start_year)
                df_child["COUNT"] = pd.to_numeric(df_child["COUNT"], errors="coerce").fillna(0).astype(int)
                st.subheader("📈 Child Cancer Cases Over Time (Age 0–14)")
                fig = go.Figure()
                for site in df_child["SITE"].unique():
                    site_df = df_child[df_child["SITE"] == site]
                    fig.add_trace(go.Scatter(x=site_df["YEAR"], y=site_df["COUNT"], mode='lines+markers', name=site))
                fig.update_layout(title="Trend by Cancer Site", xaxis_title="Year", yaxis_title="Case Count")
                st.plotly_chart(fig, use_container_width=True)

            # --- RAG Summary ---
            st.header("📚 Research Summary (Mortality & Survival Rates)")
            rag_summary = data.get("rag_data", "")
            if isinstance(rag_summary, dict):
                rag_summary = rag_summary.get("summary", "")
            if rag_summary:
                st.markdown(rag_summary)
            else:
                st.warning("No RAG summary available.")

            # --- Web Research (Markdown string) ---
            st.header("🌐 Web Research & Clinical Trials")
            web_results = data.get("web_data", "")
            if isinstance(web_results, str) and web_results.strip():
                st.markdown(web_results, unsafe_allow_html=True)
            else:
                st.warning("No clinical trial results found.")

            summary_html = f"""
                <h1>Cancer Research Report</h1>
                <h2>Query: {query}</h2>

                <h3>📚 Research Summary</h3>
                <p>{rag_summary.replace('\n', '<br>')}</p>

                <h3>🌐 Web Research & Clinical Trials</h3>
                <p>{web_results.replace('\n', '<br>')}</p>

                <h3>📊 Snowflake Data (see dashboard)</h3>
                <p>Refer to the visual and tabular data above for full statistical results.</p>
                """

            pdf_bytes = generate_pdf(summary_html)

            st.download_button(
                label="📥 Download Full Report (PDF)",
                data=pdf_bytes,
                file_name="cancer_research_report.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"PDF generation failed: {str(e)}")

st.markdown("---")
st.markdown("Cancer Research Assistant | Powered by Multi-Agent System")
