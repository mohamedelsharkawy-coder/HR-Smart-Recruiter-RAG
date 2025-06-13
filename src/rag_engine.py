"""
RAG Engine module for processing queries and generating responses.
Handles query analysis, document retrieval, and LLM response generation.
"""

from typing import Dict, List, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain.schema import Document as LangchainDocument
from langchain_community.vectorstores import FAISS

from src.config import Config
from src.vectorstore import DocumentRetriever
from utils.helpers import is_applicant_specific, is_count_query

class RAGEngine:
    """Main RAG engine for processing queries and generating responses."""
    
    def __init__(self):
        """Initialize the RAG engine."""
        self.llm = ChatGoogleGenerativeAI(
            model=Config.LLM_MODEL_NAME,
            temperature=Config.LLM_TEMPERATURE,
        )
        self.prompt_template = self._create_prompt_template()
        self.document_retriever = DocumentRetriever()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for the RAG system."""
        template = """
You are an expert HR assistant helping recruiters find the right candidates. Use the following CV context to answer recruitment-related questions.

Context: {context}

Question: {question}

Instructions:
- Focus on recruitment-relevant information (skills, experience, education, achievements)
- When comparing candidates, be specific about their qualifications
- If asking about specific technologies/skills, mention proficiency levels when available
- Include years of experience, job titles, and company names when relevant
- If information is not available, clearly state that
- Provide actionable insights for recruitment decisions
- Format output in bullet points for readability

Answer:
"""
        return PromptTemplate(template=template, input_variables=["context", "question"])
    
    def _build_context_from_query(self, query: str, vectorstore: FAISS, applicant_names: List[str]) -> List[LangchainDocument]:
        """
        Retrieve relevant documents based on query type.
        
        Args:
            query: User query
            vectorstore: FAISS vector store
            applicant_names: List of applicant names
            
        Returns:
            List of relevant documents
        """
        # Handle count queries
        if is_count_query(query):
            count_doc = LangchainDocument(
                page_content=f"Total number of CVs/applicants in the database: {len(applicant_names)}\n\nApplicant names: {', '.join(applicant_names)}",
                metadata={"applicant": "System", "type": "count_info"}
            )
            return [count_doc]
        
        # Handle applicant-specific queries
        matched_applicant = is_applicant_specific(query, applicant_names)
        
        if matched_applicant:
            # Retrieve documents for specific applicant
            docs_with_scores = self.document_retriever.retrieve_with_scores(
                vectorstore, query, Config.MAX_SIMILARITY_DOCS
            )
            retrieved_docs = self.document_retriever.filter_documents_by_applicant(
                docs_with_scores, matched_applicant, Config.SPECIFIC_RETRIEVAL_K
            )
        else:
            # General query - retrieve from all documents
            retrieved_docs = self.document_retriever.retrieve_documents(
                vectorstore, query, Config.RETRIEVAL_K
            )
        
        return retrieved_docs
    
    def _build_context_text(self, documents: List[LangchainDocument]) -> str:
        """
        Build context text from retrieved documents.
        
        Args:
            documents: List of retrieved documents
            
        Returns:
            Formatted context text
        """
        context_parts = []
        
        for doc in documents:
            applicant_name = doc.metadata.get('applicant', 'Unknown')
            context_parts.append(f"[Applicant: {applicant_name}]\n{doc.page_content}")
        
        return "\n\n".join(context_parts)
    
    def query(self, query: str, vectorstore: FAISS, applicant_names: List[str]) -> Dict[str, any]:
        """
        Process a RAG query and return results.
        
        Args:
            query: User query
            vectorstore: FAISS vector store
            applicant_names: List of applicant names
            
        Returns:
            Dictionary with result and source documents
        """
        try:
            # Retrieve relevant documents
            context_docs = self._build_context_from_query(query, vectorstore, applicant_names)
            
            if not context_docs:
                return {
                    "result": "No relevant documents found.",
                    "source_documents": []
                }
            
            # Build context text
            context_text = self._build_context_text(context_docs)
            
            # Create and run the chain
            chain: RunnableSequence = self.prompt_template | self.llm
            
            result = chain.invoke({
                "context": context_text,
                "question": query
            })
            
            return {
                "result": result.content,
                "source_documents": context_docs
            }
            
        except Exception as e:
            return {
                "result": f"Error occurred: {str(e)}",
                "source_documents": []
            }

class QueryAnalyzer:
    """Analyzes and categorizes user queries."""
    
    @staticmethod
    def analyze_query(query: str, applicant_names: List[str]) -> Dict[str, any]:
        """
        Analyze a query and return its characteristics.
        
        Args:
            query: User query
            applicant_names: List of applicant names
            
        Returns:
            Dictionary with query analysis results
        """
        analysis = {
            "query": query,
            "is_count_query": is_count_query(query),
            "is_applicant_specific": False,
            "matched_applicant": None,
            "query_type": "general"
        }
        
        # Check for applicant-specific queries
        matched_applicant = is_applicant_specific(query, applicant_names)
        if matched_applicant:
            analysis["is_applicant_specific"] = True
            analysis["matched_applicant"] = matched_applicant
            analysis["query_type"] = "applicant_specific"
        
        # Check for count queries
        if analysis["is_count_query"]:
            analysis["query_type"] = "count"
        
        return analysis
    
    @staticmethod
    def get_query_suggestions(applicant_names: List[str]) -> List[str]:
        """
        Generate query suggestions based on available applicants.
        
        Args:
            applicant_names: List of applicant names
            
        Returns:
            List of suggested queries
        """
        suggestions = [
            "Who has experience in machine learning?",
            "Compare the experience levels of all candidates",
            "How many candidates have Python experience?",
            "Who graduated from engineering faculty?",
            "What are the technical skills of all candidates?"
        ]
        
        # Add applicant-specific suggestions
        if applicant_names:
            first_applicant = applicant_names[0]
            suggestions.append(f"What are {first_applicant}'s technical skills?")
            suggestions.append(f"Tell me about {first_applicant}'s work experience")
        
        return suggestions