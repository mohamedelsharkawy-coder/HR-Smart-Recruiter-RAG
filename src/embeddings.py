"""
Embeddings module containing custom embedding classes.
Handles text embedding for the RAG system using E5 model.
"""

from langchain_community.embeddings import HuggingFaceEmbeddings
from src.config import Config

class E5Embeddings(HuggingFaceEmbeddings):
    """
    Custom E5 embeddings class that adds prefixes for better retrieval performance.
    E5 models perform better when documents are prefixed with 'passage:' and queries with 'query:'.
    """
    
    def __init__(self, model_name: str = None, **kwargs):
        """
        Initialize E5 embeddings.
        
        Args:
            model_name: Name of the E5 model to use
            **kwargs: Additional arguments for HuggingFaceEmbeddings
        """
        if model_name is None:
            model_name = Config.EMBEDDING_MODEL_NAME
        
        # Set default model kwargs if not provided
        if 'model_kwargs' not in kwargs:
            kwargs['model_kwargs'] = {"device": "cpu"}
        
        if 'encode_kwargs' not in kwargs:
            kwargs['encode_kwargs'] = {"normalize_embeddings": True}
        
        super().__init__(model_name=model_name, **kwargs)
    
    def embed_documents(self, texts):
        """
        Embed documents with 'passage:' prefix for better retrieval.
        
        Args:
            texts: List of document texts to embed
            
        Returns:
            List of embeddings
        """
        prefixed_texts = [f"passage: {text}" for text in texts]
        return super().embed_documents(prefixed_texts)

    def embed_query(self, text):
        """
        Embed query with 'query:' prefix for better retrieval.
        
        Args:
            text: Query text to embed
            
        Returns:
            Query embedding
        """
        return super().embed_query(f"query: {text}")

class EmbeddingFactory:
    """Factory class for creating different types of embeddings."""
    
    @staticmethod
    def create_e5_embeddings(**kwargs) -> E5Embeddings:
        """
        Create E5 embeddings with default configuration.
        
        Args:
            **kwargs: Additional arguments for E5Embeddings
            
        Returns:
            Configured E5Embeddings instance
        """
        return E5Embeddings(**kwargs)
    
    @staticmethod
    def create_default_embeddings() -> E5Embeddings:
        """
        Create default embeddings for the application.
        
        Returns:
            Default configured embeddings
        """
        return E5Embeddings(
            model_name=Config.EMBEDDING_MODEL_NAME,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )