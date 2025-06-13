"""
Configuration module for HR Smart Recruiter RAG system.
Contains environment variables, constants, and application settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration class."""
    
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Model configurations
    EMBEDDING_MODEL_NAME = "intfloat/e5-large-v2"
    LLM_MODEL_NAME = "gemini-2.0-flash-exp"
    LLM_TEMPERATURE = 0.5
    
    # Text processing settings
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 50
    
    # Retrieval settings
    RETRIEVAL_K = 20
    SPECIFIC_RETRIEVAL_K = 5
    MAX_SIMILARITY_DOCS = 100
    
    # UI settings
    PAGE_TITLE = "Smart Recruiter"
    PAGE_LAYOUT = "wide"
    APP_TITLE = "🤖 HR Smart Recruiter RAG"
    APP_DESCRIPTION = "Analyze candidate CVs with LLM-powered retrieval and querying"
    
    # File settings
    SUPPORTED_FILE_TYPES = ["pdf", "docx"]
    CSS_FILE_PATH = "static/styles.css"
    
    # Query keywords
    COUNT_KEYWORDS = ['how many', 'count', 'number of', 'total', 'how much']
    CV_KEYWORDS = ['cv', 'cvs', 'resume', 'resumes', 'applicant', 'applicants', 'candidate', 'candidates']

# Set environment variable for Google API
if Config.GOOGLE_API_KEY:
    os.environ["GOOGLE_API_KEY"] = Config.GOOGLE_API_KEY