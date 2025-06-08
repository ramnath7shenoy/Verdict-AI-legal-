import streamlit as st
from pathlib import Path
from app.summarizer import LegalDocumentSummarizer
from app.utils import save_uploaded_file
from app.config import API_KEY

def main():
    st.set_page_config(
        page_title="Legal Document Assistant",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("⚖️ Legal Document Assistant")
    st.subheader("Powered by Gemini Pro + FAISS Vector Search")

    if API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        st.error("❌ Please set your Gemini API key in `config.py`.")
        st.stop()

    # --- Initialize Assistant ---
    if 'assistant' not in st.session_state:
        with st.spinner("Initializing Legal Document Assistant..."):
            try:
                st.session_state.assistant = LegalDocumentSummarizer(API_KEY)
                st.success("✅ Assistant initialized successfully!")
            except Exception as e:
                st.error("❌ Failed to initialize assistant.")
                st.exception(e)
                st.stop()

    # --- Sidebar: Upload File ---
    st.sidebar.header("📁 Document Upload")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a legal document",
        type=['pdf', 'docx', 'txt'],
        help="Upload PDF, DOCX, or TXT files"
    )

    if uploaded_file:
        file_path = save_uploaded_file(uploaded_file)
        if not file_path:
            st.stop()

        st.sidebar.success(f"✅ Uploaded: {uploaded_file.name}")
        st.sidebar.info(f"📊 Size: {len(uploaded_file.getvalue())} bytes")

        tab1, tab2 = st.tabs(["📋 Document Summarization", "❓ Document Query"])

        # --- Summarization Tab ---
        with tab1:
            st.header("📋 Document Summarization")
            col1, col2 = st.columns([2, 1])

            with col1:
                summary_type = st.selectbox(
                    "Choose Summary Type:",
                    options=[
                        ("executive", "Executive Summary"),
                        ("detailed", "Detailed Summary"),
                        ("key_points", "Key Points"),
                        ("roles_parties", "Roles & Parties"),
                        ("timeline", "Timeline"),
                        ("risk_analysis", "Risk Analysis"),
                        ("comprehensive", "Comprehensive Analysis"),
                        ("custom", "Custom Prompt")
                    ],
                    format_func=lambda x: x[1]
                )

            custom_prompt = None
            if summary_type[0] == "custom":
                custom_prompt = st.text_area(
                    "Enter your custom prompt:",
                    height=100,
                    placeholder="Describe what specific analysis you want..."
                )

            if st.button("🔍 Generate Summary"):
                if summary_type[0] == "custom" and not custom_prompt:
                    st.error("Please enter a custom prompt.")
                else:
                    with st.spinner("Generating summary..."):
                        try:
                            summary = st.session_state.assistant.summarize_document(
                                file_path, summary_type[0], custom_prompt
                            )
                            st.subheader("📄 Summary Result")
                            st.markdown(summary)

                            st.download_button(
                                label="💾 Download Summary",
                                data=summary,
                                file_name=f"summary_{Path(uploaded_file.name).stem}_{summary_type[0]}.txt",
                                mime="text/plain"
                            )
                        except Exception as e:
                            st.error("❌ Error generating summary.")
                            st.exception(e)

        # --- Query Tab ---
        with tab2:
            st.header("❓ Document Query with Similar Cases")
            st.info("Ask questions about your document. The system will search for similar documents in the FAISS database to provide context.")

            col1, col2 = st.columns([3, 1])
            with col1:
                query = st.text_input(
                    "Enter your question:",
                    placeholder="What are the key obligations in this contract?"
                )
            with col2:
                k = st.number_input(
                    "Similar docs to retrieve:",
                    min_value=1,
                    max_value=20,
                    value=5
                )

            if st.button("🔍 Query Document"):
                if not query:
                    st.error("Please enter a question.")
                else:
                    with st.spinner("Processing query and searching similar documents..."):
                        try:
                            answer = st.session_state.assistant.query_document(file_path, query, k)
                            st.subheader("💡 Answer")
                            st.markdown(answer)

                            st.download_button(
                                label="💾 Download Answer",
                                data=f"Question: {query}\n\n{answer}",
                                file_name=f"query_result_{Path(uploaded_file.name).stem}.txt",
                                mime="text/plain"
                            )
                        except Exception as e:
                            st.error("❌ Error processing query.")
                            st.exception(e)
    else:
        st.info("👆 Please upload a legal document to get started")
        st.markdown("""
        ### 🔎 Features:
        - **Document Summarization**: Executive summaries, key points, timelines, and more
        - **Natural Language Querying**: Ask questions and get relevant insights
        - **Vector Search with FAISS**: Enhances answers with context from similar documents
        - **Supported Files**: PDF, DOCX, TXT
        """)

if __name__ == "__main__":
    main()
