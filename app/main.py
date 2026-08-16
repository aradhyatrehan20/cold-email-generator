
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
  st.title("📧 AI Cold Email Generator")

  st.markdown("""
  Generate personalized cold emails for job postings using **LLM + ChromaDB + LangChain**.

  Paste a career page URL below and let AI draft a tailored business email.  
  """)
  url_input = st.text_input(
    "🔗 Enter Job Posting URL",
    placeholder="Paste any careers page URL..."
    )
  submit_button = st.button(
    "🚀 Generate Email",
    use_container_width=True
    )

  if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)

            st.subheader("📧 Generated Email")

            st.text_area(
             "Email",
            value=email,
            height=400
)
            
            st.download_button(
    label="📥 Download Email",
    data=email,
    file_name="cold_email.txt",
    mime="text/plain"
)
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
