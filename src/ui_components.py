"""
UI Components module for Streamlit interface.
Contains reusable UI components and styling functions.
"""

import streamlit as st
from typing import List, Dict, Any
from src.config import Config

class UIComponents:
    """Collection of reusable UI components."""
    
    @staticmethod
    def setup_page_config():
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title=Config.PAGE_TITLE,
            layout=Config.PAGE_LAYOUT
        )
    
    @staticmethod
    def load_custom_css():
        """Load custom CSS styles."""
        try:
            with open(Config.CSS_FILE_PATH) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except FileNotFoundError:
            st.warning("CSS file not found. Using default styling.")
    
    @staticmethod
    def render_header():
        """Render the application header."""
        st.markdown(f"""
        <div class="header">
            <h1>{Config.APP_TITLE}</h1>
            <p>{Config.APP_DESCRIPTION}</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_file_uploader():
        """Render the file uploader component."""
        return st.sidebar.file_uploader(
            "Upload CVs (PDFs and DOCX)", 
            type=Config.SUPPORTED_FILE_TYPES, 
            accept_multiple_files=True
        )
    
    @staticmethod
    def render_sidebar_title():
        """Render sidebar title."""
        st.sidebar.title("Settings")
    
    @staticmethod
    def render_database_info(applicant_names: List[str]):
        """
        Render database information in sidebar.
        
        Args:
            applicant_names: List of applicant names
        """
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Database Info")
        st.sidebar.write(f"**Total CVs:** {len(applicant_names)}")
        st.sidebar.write("**Applicants:**")
        for name in applicant_names:
            st.sidebar.write(f"• {name}")
    
    @staticmethod
    def render_query_examples():
        """Render example queries in an expander."""
        with st.expander("💡 Example Queries"):
            st.write("""
            - **General**: "Who has experience in machine learning?"
            - **Specific**: "What are John Smith's technical skills?"
            - **Count**: "How many candidates have Python experience?"
            - **Comparison**: "Compare the experience levels of all candidates"
            - **Education**: "Who graduated from engineering faculty?"
            """)
    
    @staticmethod
    def render_query_input() -> str:
        """
        Render query input field.
        
        Returns:
            User query string
        """
        return st.text_input("Enter your query:")
    
    @staticmethod
    def render_results(result: str, source_documents: List[Any]):
        """
        Render query results and source documents.
        
        Args:
            result: Generated answer
            source_documents: List of source documents
        """
        # Render answer
        st.markdown("""<div class='section'><h4>🎯 Answer</h4></div>""", unsafe_allow_html=True)
        st.write(result)
        
        # Render source documents
        if source_documents:
            st.markdown("""<div class='section'><h4>📚 Source CV Highlights</h4></div>""", unsafe_allow_html=True)
            UIComponents._render_source_documents(source_documents)
    
    @staticmethod
    def _render_source_documents(source_documents: List[Any]):
        """
        Render source documents with highlights.
        
        Args:
            source_documents: List of source documents
        """
        seen_names = set()
        
        for doc in source_documents:
            applicant_name = doc.metadata.get("applicant", "Unknown")
            if applicant_name in seen_names:
                continue
            seen_names.add(applicant_name)

            st.markdown(f"""
            <div class="card">
                <h5>{applicant_name}</h5>
                <p><b>Type:</b> {doc.metadata.get("type", "CV Content")}</p>
                <p><b>Preview:</b> {doc.page_content[:400]}...</p>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def render_instructions():
        """Render instructions when no data is loaded."""
        st.info("Please upload and index CVs before asking questions.")
        
        st.markdown("""
        <div class="section">
            <h3>📋 How to Use</h3>
            <ol>
                <li><strong>Upload CVs:</strong> Use the sidebar to upload PDF or DOCX files</li>
                <li><strong>Index CVs:</strong> Click "Load & Index CVs" to process the documents</li>
                <li><strong>Ask Questions:</strong> Enter queries about the candidates</li>
                <li><strong>Get Insights:</strong> Review the AI-powered answers and source highlights</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_loading_spinner(message: str):
        """
        Render loading spinner with message.
        
        Args:
            message: Loading message to display
        """
        return st.spinner(message)
    
    @staticmethod
    def show_success_message(message: str):
        """Show success message."""
        st.success(message)
    
    @staticmethod
    def show_error_message(message: str):
        """Show error message."""
        st.error(message)
    
    @staticmethod
    def show_warning_message(message: str):
        """Show warning message."""
        st.warning(message)
    
    @staticmethod
    def show_info_message(message: str):
        """Show info message."""
        st.info(message)

class SessionManager:
    """Manages Streamlit session state."""
    
    @staticmethod
    def initialize_session_state():
        """Initialize session state variables."""
        if 'vectorstore' not in st.session_state:
            st.session_state.vectorstore = None
        if 'applicant_names' not in st.session_state:
            st.session_state.applicant_names = []
        if 'applicant_cvs' not in st.session_state:
            st.session_state.applicant_cvs = {}
    
    @staticmethod
    def update_vectorstore(vectorstore, applicant_names: List[str], applicant_cvs: Dict[str, str]):
        """
        Update session state with new vectorstore data.
        
        Args:
            vectorstore: FAISS vectorstore
            applicant_names: List of applicant names
            applicant_cvs: Dictionary of applicant CVs
        """
        st.session_state.vectorstore = vectorstore
        st.session_state.applicant_names = applicant_names
        st.session_state.applicant_cvs = applicant_cvs
    
    @staticmethod
    def has_vectorstore() -> bool:
        """Check if vectorstore exists in session state."""
        return (hasattr(st.session_state, 'vectorstore') and 
                st.session_state.vectorstore is not None)
    
    @staticmethod
    def get_vectorstore():
        """Get vectorstore from session state."""
        return getattr(st.session_state, 'vectorstore', None)
    
    @staticmethod
    def get_applicant_names() -> List[str]:
        """Get applicant names from session state."""
        return getattr(st.session_state, 'applicant_names', [])
    
    @staticmethod
    def get_applicant_cvs() -> Dict[str, str]:
        """Get applicant CVs from session state."""
        return getattr(st.session_state, 'applicant_cvs', {})