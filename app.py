"""
Main Streamlit application for HR Smart Recruiter RAG system.
This is the entry point that orchestrates all components.
"""

import streamlit as st
from src import (
    Config, DocumentProcessor, VectorStoreManager, RAGEngine,
    UIComponents, SessionManager, QueryAnalyzer
)
from utils.helpers import validate_api_key

def initialize_app():
    """Initialize the Streamlit application."""
    # Setup page configuration
    UIComponents.setup_page_config()
    
    # Load custom CSS
    UIComponents.load_custom_css()
    
    # Initialize session state
    SessionManager.initialize_session_state()
    
    # Validate API key
    if not validate_api_key():
        st.error("❌ Google API key not found. Please set GOOGLE_API_KEY in your .env file.")
        st.stop()

def render_main_interface():
    """Render the main application interface."""
    # Render header
    UIComponents.render_header()
    
    # Check if vectorstore exists
    if SessionManager.has_vectorstore():
        render_query_interface()
    else:
        UIComponents.render_instructions()

def render_sidebar():
    """Render the sidebar with file upload and settings."""
    UIComponents.render_sidebar_title()
    
    # File uploader
    uploaded_files = UIComponents.render_file_uploader()
    
    # Load & Index button
    if st.sidebar.button("🔄 Load & Index CVs"):
        handle_file_upload(uploaded_files)
    
    # Show database info if vectorstore exists
    if SessionManager.has_vectorstore():
        applicant_names = SessionManager.get_applicant_names()
        UIComponents.render_database_info(applicant_names)

def handle_file_upload(uploaded_files):
    """
    Handle file upload and indexing process.
    
    Args:
        uploaded_files: List of uploaded files from Streamlit
    """
    if not uploaded_files:
        UIComponents.show_warning_message("Please upload one or more CV files before indexing.")
        return
    
    with UIComponents.render_loading_spinner("Processing CVs and building vectorstore..."):
        try:
            # Extract text from files
            document_processor = DocumentProcessor()
            applicant_cvs = document_processor.extract_text_from_files(uploaded_files)
            
            if not applicant_cvs:
                UIComponents.show_error_message("❌ No valid CV files found.")
                return
            
            # Create vectorstore
            vectorstore_manager = VectorStoreManager()
            vectorstore = vectorstore_manager.create_vectorstore(applicant_cvs)
            
            if vectorstore:
                # Update session state
                applicant_names = list(applicant_cvs.keys())
                SessionManager.update_vectorstore(vectorstore, applicant_names, applicant_cvs)
                
                # Show success message
                UIComponents.show_success_message(f"✅ Successfully indexed {len(applicant_cvs)} CVs!")
                UIComponents.show_info_message(f"📋 Loaded applicants: {', '.join(applicant_names)}")
            else:
                UIComponents.show_error_message("❌ Failed to create vectorstore")
                
        except Exception as e:
            UIComponents.show_error_message(f"❌ Error: {str(e)}")

def render_query_interface():
    """Render the query interface when vectorstore is available."""
    st.markdown("""<div class="section"><h3>Ask Your Question</h3></div>""", unsafe_allow_html=True)
    
    # Show example queries
    UIComponents.render_query_examples()
    
    # Query input
    user_query = UIComponents.render_query_input()
    
    # Query button and processing
    if st.button("🔍 Run Query") and user_query:
        handle_query(user_query)

def handle_query(user_query: str):
    """
    Handle user query processing.
    
    Args:
        user_query: User's query string
    """
    with UIComponents.render_loading_spinner("Retrieving relevant candidates..."):
        try:
            # Get data from session state
            vectorstore = SessionManager.get_vectorstore()
            applicant_names = SessionManager.get_applicant_names()
            
            # Initialize RAG engine
            rag_engine = RAGEngine()
            
            # Process query
            result = rag_engine.query(user_query, vectorstore, applicant_names)
            
            # Render results
            UIComponents.render_results(result["result"], result["source_documents"])
            
        except Exception as e:
            UIComponents.show_error_message(f"❌ Error processing query: {str(e)}")

def main():
    """Main application function."""
    try:
        # Initialize the application
        initialize_app()
        
        # Render sidebar
        render_sidebar()
        
        # Render main interface
        render_main_interface()
        
    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        st.error("Please check your configuration and try again.")

if __name__ == "__main__":
    main()