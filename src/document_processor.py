"""
Document processing module for extracting text from PDF and DOCX files.
Handles file uploads and text extraction for the RAG system.
"""

import os
from typing import Dict, List
from PyPDF2 import PdfReader
from docx import Document
from utils.helpers import extract_person_name

class DocumentProcessor:
    """Handles document processing and text extraction."""
    
    @staticmethod
    def extract_text_from_pdf(file) -> str:
        """Extract text from a PDF file."""
        try:
            reader = PdfReader(file)
            text = "\n".join(page.extract_text() or '' for page in reader.pages)
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF file: {str(e)}")
    
    @staticmethod
    def extract_text_from_docx(file) -> str:
        """Extract text from a DOCX file."""
        try:
            doc = Document(file)
            text = "\n".join(p.text for p in doc.paragraphs)
            return text
        except Exception as e:
            raise Exception(f"Error reading DOCX file: {str(e)}")
    
    @classmethod
    def extract_text_from_files(cls, uploaded_files) -> Dict[str, str]:
        """
        Extract text from uploaded PDF and DOCX files.
        
        Args:
            uploaded_files: List of uploaded files from Streamlit
            
        Returns:
            Dict mapping applicant names to their CV text
        """
        applicant_cvs = {}
        
        for uploaded_file in uploaded_files:
            applicant_name = extract_person_name(uploaded_file.name)
            
            try:
                if uploaded_file.type == "application/pdf":
                    text = cls.extract_text_from_pdf(uploaded_file)
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    text = cls.extract_text_from_docx(uploaded_file)
                else:
                    continue  # Skip unsupported file types
                
                applicant_cvs[applicant_name] = text
                
            except Exception as e:
                # Log the error but continue processing other files
                print(f"Warning: Could not process file {uploaded_file.name}: {str(e)}")
                continue
        
        return applicant_cvs
    
    @staticmethod
    def validate_files(uploaded_files) -> List[str]:
        """
        Validate uploaded files and return list of errors if any.
        
        Args:
            uploaded_files: List of uploaded files
            
        Returns:
            List of validation error messages
        """
        errors = []
        
        if not uploaded_files:
            errors.append("No files uploaded")
            return errors
        
        supported_types = [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ]
        
        for file in uploaded_files:
            if file.type not in supported_types:
                errors.append(f"Unsupported file type: {file.name}")
        
        return errors