"""
Helper functions for the HR Smart Recruiter application.
Contains utility functions for query processing and text manipulation.
"""

import os
from typing import List, Optional
from src.config import Config

def extract_person_name(filename: str) -> str:
    """
    Extract person name from filename by removing extension.
    
    Args:
        filename: Name of the file
        
    Returns:
        Person name without extension
    """
    name, _ = os.path.splitext(filename)
    return name.strip()

def is_applicant_specific(query: str, applicant_names: List[str]) -> Optional[str]:
    """
    Check if query is specific to a particular applicant.
    
    Args:
        query: User query
        applicant_names: List of applicant names
        
    Returns:
        Matched applicant name or None
    """
    query_lower = query.lower()
    for name in applicant_names:
        if name.lower() in query_lower:
            return name
    return None

def is_count_query(query: str) -> bool:
    """
    Check if query is asking for count/number information.
    
    Args:
        query: User query
        
    Returns:
        True if it's a count query, False otherwise
    """
    query_lower = query.lower()
    
    has_count_keyword = any(
        keyword in query_lower for keyword in Config.COUNT_KEYWORDS
    )
    has_cv_keyword = any(
        keyword in query_lower for keyword in Config.CV_KEYWORDS
    )
    
    return has_count_keyword and has_cv_keyword

def clean_text(text: str) -> str:
    """
    Clean and normalize text content.
    
    Args:
        text: Raw text content
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace and normalize
    text = ' '.join(text.split())
    
    # Remove common PDF artifacts
    text = text.replace('\x00', '')  # Remove null characters
    text = text.replace('\ufffd', '')  # Remove replacement characters
    
    return text.strip()

def validate_api_key() -> bool:
    """
    Validate that required API keys are present.
    
    Returns:
        True if API key is valid, False otherwise
    """
    return bool(Config.GOOGLE_API_KEY and Config.GOOGLE_API_KEY.strip())

def format_applicant_list(applicant_names: List[str]) -> str:
    """
    Format list of applicant names for display.
    
    Args:
        applicant_names: List of applicant names
        
    Returns:
        Formatted string
    """
    if not applicant_names:
        return "No applicants"
    
    if len(applicant_names) == 1:
        return applicant_names[0]
    elif len(applicant_names) == 2:
        return f"{applicant_names[0]} and {applicant_names[1]}"
    else:
        return f"{', '.join(applicant_names[:-1])}, and {applicant_names[-1]}"

def truncate_text(text: str, max_length: int = 400) -> str:
    """
    Truncate text to specified length with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + "..."

def get_file_size_mb(file) -> float:
    """
    Get file size in MB.
    
    Args:
        file: Uploaded file object
        
    Returns:
        File size in MB
    """
    try:
        return file.size / (1024 * 1024)
    except:
        return 0.0

def validate_file_size(file, max_size_mb: float = 10.0) -> bool:
    """
    Validate file size.
    
    Args:
        file: Uploaded file object
        max_size_mb: Maximum allowed size in MB
        
    Returns:
        True if file size is valid, False otherwise
    """
    return get_file_size_mb(file) <= max_size_mb