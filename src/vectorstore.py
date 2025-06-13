"""
Vector store module for creating and managing FAISS vector databases.
Handles document chunking, embedding, and vector store operations.
"""

from typing import Dict, List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.schema import Document as LangchainDocument
from src.embeddings import EmbeddingFactory
from src.config import Config

class VectorStoreManager:
    """Manages vector store operations for the RAG system."""
    
    def __init__(self):
        """Initialize the vector store manager."""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
        self.embedding_model = EmbeddingFactory.create_default_embeddings()
    
    def create_documents_from_cvs(self, applicant_cvs: Dict[str, str]) -> List[LangchainDocument]:
        """
        Create LangChain documents from CV texts with metadata.
        
        Args:
            applicant_cvs: Dictionary mapping applicant names to CV texts
            
        Returns:
            List of LangChain documents with metadata
        """
        all_documents = []
        
        for applicant_name, cv_text in applicant_cvs.items():
            # Create chunks with metadata
            chunks = self.text_splitter.create_documents(
                [cv_text], 
                metadatas=[{"applicant": applicant_name}]
            )
            all_documents.extend(chunks)
        
        return all_documents
    
    def create_vectorstore(self, applicant_cvs: Dict[str, str]) -> Optional[FAISS]:
        """
        Create a FAISS vector store from applicant CVs.
        
        Args:
            applicant_cvs: Dictionary mapping applicant names to CV texts
            
        Returns:
            FAISS vector store or None if creation fails
        """
        try:
            # Create documents
            documents = self.create_documents_from_cvs(applicant_cvs)
            
            if not documents:
                return None
            
            # Create vector store
            vectorstore = FAISS.from_documents(documents, self.embedding_model)
            return vectorstore
            
        except Exception as e:
            print(f"Error creating vector store: {str(e)}")
            return None
    
    def add_documents_to_vectorstore(self, vectorstore: FAISS, new_cvs: Dict[str, str]) -> FAISS:
        """
        Add new documents to an existing vector store.
        
        Args:
            vectorstore: Existing FAISS vector store
            new_cvs: New CV texts to add
            
        Returns:
            Updated vector store
        """
        try:
            new_documents = self.create_documents_from_cvs(new_cvs)
            if new_documents:
                vectorstore.add_documents(new_documents)
            return vectorstore
            
        except Exception as e:
            print(f"Error adding documents to vector store: {str(e)}")
            return vectorstore
    
    def get_vectorstore_info(self, vectorstore: FAISS) -> Dict[str, int]:
        """
        Get information about the vector store.
        
        Args:
            vectorstore: FAISS vector store
            
        Returns:
            Dictionary with vector store statistics
        """
        try:
            # Get the number of vectors in the store
            index_info = vectorstore.index.ntotal if hasattr(vectorstore, 'index') else 0
            
            return {
                "total_documents": index_info,
                "embedding_dimension": vectorstore.index.d if hasattr(vectorstore, 'index') else 0
            }
        except Exception as e:
            print(f"Error getting vector store info: {str(e)}")
            return {"total_documents": 0, "embedding_dimension": 0}

class DocumentRetriever:
    """Handles document retrieval from vector stores."""
    
    @staticmethod
    def retrieve_documents(vectorstore: FAISS, query: str, k: int = None) -> List[LangchainDocument]:
        """
        Retrieve documents from vector store based on similarity.
        
        Args:
            vectorstore: FAISS vector store
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            List of retrieved documents
        """
        if k is None:
            k = Config.RETRIEVAL_K
        
        try:
            retriever = vectorstore.as_retriever(search_kwargs={"k": k})
            docs = retriever.get_relevant_documents(query)
            return docs
        except Exception as e:
            print(f"Error retrieving documents: {str(e)}")
            return []
    
    @staticmethod
    def retrieve_with_scores(vectorstore: FAISS, query: str, k: int = None) -> List[tuple]:
        """
        Retrieve documents with similarity scores.
        
        Args:
            vectorstore: FAISS vector store
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            List of (document, score) tuples
        """
        if k is None:
            k = Config.MAX_SIMILARITY_DOCS
        
        try:
            docs_with_scores = vectorstore.similarity_search_with_score(query, k=k)
            return docs_with_scores
        except Exception as e:
            print(f"Error retrieving documents with scores: {str(e)}")
            return []
    
    @staticmethod
    def filter_documents_by_applicant(docs_with_scores: List[tuple], applicant_name: str, k: int = None) -> List[LangchainDocument]:
        """
        Filter documents by specific applicant name.
        
        Args:
            docs_with_scores: List of (document, score) tuples
            applicant_name: Name of the applicant to filter by
            k: Maximum number of documents to return
            
        Returns:
            List of filtered documents
        """
        if k is None:
            k = Config.SPECIFIC_RETRIEVAL_K
        
        filtered_docs = [
            doc for doc, score in docs_with_scores 
            if doc.metadata.get('applicant', '').lower() == applicant_name.lower()
        ]
        
        return filtered_docs[:k]