"""
Semantic search module for Ragatanga.

This module provides semantic search functionality using embeddings.
"""

import os
import asyncio
from typing import List, Tuple, Optional
from loguru import logger
import numpy as np

# Import faiss properly
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logger.warning("FAISS not available. Install it with 'pip install faiss-cpu' or 'pip install faiss-gpu'")

from ragatanga.config import DEFAULT_CHUNK_SIZE as CHUNK_SIZE
from ragatanga.config import DEFAULT_CHUNK_OVERLAP as CHUNK_OVERLAP
from ragatanga.utils.embeddings import EmbeddingProvider, build_faiss_index, save_faiss_index, load_faiss_index
from ragatanga.utils.text import split_text, CHONKIE_AVAILABLE

class SemanticSearch:
    """
    Semantic search implementation for retrieving knowledge base entries.
    """
    
    def __init__(self, embed_provider=None, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
        """
        Initialize the semantic search.
        
        Args:
            embed_provider: Embedding provider to use
            chunk_size: Maximum size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.embed_provider = embed_provider or EmbeddingProvider.get_provider()
        # Get dimension from provider or use default value
        self.dimension = getattr(self.embed_provider, 'dimension', 1536)  # Default to OpenAI's dimension
        self.kbase_entries = []
        self.kbase_index = None
        self.kbase_embeddings = None
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    async def load_knowledge_base(self, kb_path: str, force_rebuild: bool = False) -> None:
        """
        Load a knowledge base from a file and build or load a FAISS index.
        
        Args:
            kb_path: Path to the knowledge base file
            force_rebuild: Whether to force rebuilding the index
        """
        try:
            # Verify the knowledge base file exists
            if not os.path.exists(kb_path):
                logger.error(f"Knowledge base file not found: {kb_path}")
                return
                
            # Create index directory if it doesn't exist
            index_dir = os.path.join(os.path.dirname(kb_path), "index")
            os.makedirs(index_dir, exist_ok=True)
            
            # Define paths for index and embedding files
            base_name = os.path.basename(kb_path).split('.')[0]
            index_file = os.path.join(index_dir, f"{base_name}.index")
            embed_file = os.path.join(index_dir, f"{base_name}.npy")
            
            # Read the knowledge base file
            with open(kb_path, 'r', encoding='utf-8') as f:
                kbase_content = f.read()
            
            # Use enhanced text chunking with Chonkie if available
            file_ext = kb_path.lower().split('.')[-1] if '.' in kb_path else ''
            
            if file_ext == 'md':
                # Use markdown-aware chunking for markdown files
                chunking_method = "markdown" if CHONKIE_AVAILABLE else "legacy"
            else:
                # Use recursive chunking for other text files
                chunking_method = "recursive" if CHONKIE_AVAILABLE else "legacy"
            
            # Split the content into chunks
            self.kbase_entries = split_text(
                kbase_content, 
                max_chunk_size=self.chunk_size,
                overlap=self.chunk_overlap,
                chunking_method=chunking_method
            )
            
            logger.info(f"Loaded {len(self.kbase_entries)} entries from knowledge base")
            
            # Build or load FAISS index
            if not force_rebuild and os.path.exists(index_file) and os.path.exists(embed_file):
                logger.info("Loading existing FAISS index and embeddings")
                try:
                    self.kbase_index, self.kbase_embeddings = load_faiss_index(index_file, embed_file)
                    # Verify the index is properly loaded
                    if self.kbase_index is None:
                        logger.warning("Failed to load existing index, rebuilding...")
                        raise Exception("Index loading failed")
                    else:
                        logger.info("FAISS index successfully loaded")
                except Exception as e:
                    logger.warning(f"Error loading index: {str(e)}. Rebuilding index...")
                    force_rebuild = True
            
            # If index should be rebuilt or loading failed
            if force_rebuild or self.kbase_index is None:
                logger.info("Building new FAISS index")
                if len(self.kbase_entries) == 0:
                    logger.warning("No entries to index! The knowledge base may be empty.")
                    # Initialize empty index to avoid None errors
                    self.kbase_embeddings = np.zeros((0, self.dimension), dtype=np.float32)
                    self.kbase_index = faiss.IndexFlatL2(self.dimension)
                    # Need to add empty embeddings to the index even when empty
                    if len(self.kbase_embeddings) > 0:
                        self.kbase_index.add(self.kbase_embeddings)  # type: ignore
                else:
                    self.kbase_embeddings = await self.embed_provider.embed_texts(self.kbase_entries)
                    self.kbase_index, self.kbase_embeddings = build_faiss_index(self.kbase_embeddings, self.dimension)
                    save_faiss_index(self.kbase_index, index_file, self.kbase_embeddings, embed_file)
                    logger.info("FAISS index successfully built and saved")
            
            # Final verification
            if self.kbase_index is None:
                logger.error("Failed to initialize knowledge base index")
            
        except Exception as e:
            logger.error(f"Error loading knowledge base: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            # Initialize empty index to avoid None errors
            self.kbase_entries = []
            self.kbase_embeddings = np.zeros((0, self.dimension), dtype=np.float32)
            # Initialize IndexFlatL2 properly
            self.kbase_index = faiss.IndexFlatL2(self.dimension)
            # Need to add empty embeddings to the index even when empty
            if len(self.kbase_embeddings) > 0:
                self.kbase_index.add(self.kbase_embeddings)  # type: ignore
    
    async def index_documents(self, documents: List[str]) -> None:
        """
        Index a list of documents.
        
        Args:
            documents: List of document texts to index
        """
        if not documents:
            logger.warning("No documents to index")
            return
            
        try:
            # Store the documents
            self.kbase_entries = documents
            
            # Generate embeddings
            self.kbase_embeddings = await self.embed_provider.embed_texts(documents)
            
            # Build the index
            self.kbase_index, self.kbase_embeddings = build_faiss_index(self.kbase_embeddings, self.dimension)
            
            logger.info(f"Successfully indexed {len(documents)} documents")
        except Exception as e:
            logger.error(f"Error indexing documents: {str(e)}")
            raise
    
    def _chunk_entries(self, entries: List[str], max_tokens: int = CHUNK_SIZE) -> List[str]:
        """
        Further chunk entries to ensure they don't exceed token limits.
        
        Args:
            entries: List of text entries
            max_tokens: Maximum tokens per chunk (conservative estimate)
            
        Returns:
            List of chunked entries
        """
        import re
        chunked_entries = []
        
        for entry in entries:
            # Estimate token count (rough estimation: 4 chars ~= 1 token)
            estimated_tokens = len(entry) / 4
            
            if estimated_tokens <= max_tokens:
                chunked_entries.append(entry)
            else:
                # Split long entries into paragraphs
                paragraphs = re.split(r'\n\s*\n', entry)
                
                current_chunk: List[str] = []
                current_length: float = 0.0
                
                for para in paragraphs:
                    para_tokens = len(para) / 4
                    
                    # If adding this paragraph exceeds the limit, save the current chunk and start a new one
                    if current_length + para_tokens > max_tokens and current_chunk:
                        chunked_entries.append('\n\n'.join(current_chunk))
                        current_chunk = []
                        current_length = 0.0
                    
                    # If a single paragraph is too long, split it into sentences
                    if para_tokens > max_tokens:
                        sentences = re.split(r'(?<=[.!?])\s+', para)
                        
                        for sentence in sentences:
                            sentence_tokens = len(sentence) / 4
                            
                            # If adding this sentence exceeds the limit, save the current chunk and start a new one
                            if current_length + sentence_tokens > max_tokens and current_chunk:
                                chunked_entries.append('\n\n'.join(current_chunk))
                                current_chunk = []
                                current_length = 0.0
                            
                            # If a single sentence is still too long (rare), force split it
                            if sentence_tokens > max_tokens:
                                words = sentence.split()
                                temp_chunk: List[str] = []
                                temp_length: float = 0.0
                                
                                for word in words:
                                    word_tokens = len(word) / 4
                                    
                                    if temp_length + word_tokens > max_tokens and temp_chunk:
                                        current_chunk.append(' '.join(temp_chunk))
                                        current_length += temp_length
                                        
                                        # If the current chunk is now full, save it and start a new one
                                        if current_length > max_tokens:
                                            chunked_entries.append('\n\n'.join(current_chunk))
                                            current_chunk = []
                                            current_length = 0.0
                                            
                                        temp_chunk = []
                                        temp_length = 0.0
                                    
                                    temp_chunk.append(word)
                                    temp_length += word_tokens
                                
                                # Add any remaining words
                                if temp_chunk:
                                    current_chunk.append(' '.join(temp_chunk))
                                    current_length += temp_length
                            else:
                                current_chunk.append(sentence)
                                current_length += sentence_tokens
                    else:
                        current_chunk.append(para)
                        current_length += para_tokens
                
                # Add any remaining content
                if current_chunk:
                    chunked_entries.append('\n\n'.join(current_chunk))
        
        logger.info(f"Chunked {len(entries)} original entries into {len(chunked_entries)} chunks to respect token limits")
        return chunked_entries
    
    async def search(self, query: str, k: int = 10) -> List[str]:
        """
        Search the knowledge base for entries similar to the query.
        
        Args:
            query: The query string
            k: Number of results to return
            
        Returns:
            List of matching entries
        """
        results, _ = await self.search_with_scores(query, k)
        return results
    
    async def search_with_scores(self, query: str, k: int = 10) -> Tuple[List[str], List[float]]:
        """
        Search the knowledge base and return entries with similarity scores.
        
        Args:
            query: The query string
            k: Number of results to return
            
        Returns:
            Tuple of (results, similarity_scores)
        """
        if self.kbase_index is None:
            logger.warning("Knowledge base index not initialized")
            return [], []
        
        if k > len(self.kbase_entries):
            k = len(self.kbase_entries)
            
        # Get query embedding
        q_emb = await self.embed_provider.embed_query(query)
        q_emb = q_emb.reshape(1, -1)
        
        # Search the index
        if not FAISS_AVAILABLE:
            raise ImportError("FAISS is required. Install it with 'pip install faiss-cpu' or 'pip install faiss-gpu'")
            
        def search_index():
            # Ensure index is not None before searching
            if self.kbase_index is None:
                raise ValueError("Knowledge base index is None")
                
            # FAISS search method returns distances and indices
            # We're ignoring linter errors since FAISS API doesn't match what the linter expects
            # distances, labels are return values, not parameters
            # type: ignore
            return self.kbase_index.search(q_emb, k)  # type: ignore
        
        distances, indices = await asyncio.to_thread(search_index)
        
        # Convert distances to similarity scores
        similarity_scores = distances[0].tolist()
        results = [self.kbase_entries[i] for i in indices[0].tolist()]
        
        return results, similarity_scores

    async def batch_search(self, queries: List[str], k: int = 10) -> List[List[str]]:
        """
        TODO improve implementation of batch search
        
        Search the knowledge base for multiple queries in batch.
        
        Args:
            queries: List of query strings
            k: Number of results to return per query
            
        Returns:
            List of results for each query
        """
        results = []
        for query in queries:
            query_results = await self.search(query, k)
            results.append(query_results)
        return results

async def retrieve_top_k(query: str, k: int, semantic_search: Optional[SemanticSearch] = None) -> List[str]:
    """
    Use semantic search to find the top-k most similar knowledge base entries.
    
    Args:
        query: The query string
        k: Number of results to retrieve
        semantic_search: SemanticSearch instance (if None, uses global instance)
        
    Returns:
        List of matching entries
    """
    global _semantic_search
    if semantic_search is None:
        # Try to get the properly initialized instance from the FastAPI app
        try:
            from ragatanga.api.app import app
            if hasattr(app.state, "semantic_search") and app.state.semantic_search is not None:
                semantic_search = app.state.semantic_search
                # Update the global instance to the app instance
                _semantic_search = app.state.semantic_search
            else:
                # Use existing global instance if available
                if '_semantic_search' not in globals() or _semantic_search is None:
                    logger.warning("No semantic search instance available in app state or globally")
                    return []
                semantic_search = _semantic_search
        except ImportError:
            # If we can't import app (e.g., in tests), use the global instance
            if '_semantic_search' not in globals() or _semantic_search is None:
                logger.warning("No semantic search instance available globally")
                return []
            semantic_search = _semantic_search
    
    # Ensure we have a valid semantic search instance with loaded index
    if semantic_search is None or semantic_search.kbase_index is None:
        logger.error("Failed to obtain a valid semantic search instance with loaded index")
        return []
        
    return await semantic_search.search(query, k)

async def retrieve_top_k_with_scores(query: str, k: int, semantic_search: Optional[SemanticSearch] = None) -> Tuple[List[str], List[float]]:
    """
    Use semantic search to find the top-k most similar knowledge base entries with scores.
    
    Args:
        query: The query string
        k: Number of results to retrieve
        semantic_search: SemanticSearch instance (if None, uses global instance)
        
    Returns:
        Tuple of (results, similarity_scores)
    """
    global _semantic_search
    if semantic_search is None:
        # Try to get the properly initialized instance from the FastAPI app
        try:
            from ragatanga.api.app import app
            if hasattr(app.state, "semantic_search") and app.state.semantic_search is not None:
                semantic_search = app.state.semantic_search
                # Update the global instance to the app instance
                _semantic_search = app.state.semantic_search
            else:
                # Use existing global instance if available
                if '_semantic_search' not in globals() or _semantic_search is None:
                    logger.warning("No semantic search instance available in app state or globally")
                    return [], []
                semantic_search = _semantic_search
        except ImportError:
            # If we can't import app (e.g., in tests), use the global instance
            if '_semantic_search' not in globals() or _semantic_search is None:
                logger.warning("No semantic search instance available globally")
                return [], []
            semantic_search = _semantic_search
    
    # Ensure we have a valid semantic search instance with loaded index
    if semantic_search is None or semantic_search.kbase_index is None:
        logger.error("Failed to obtain a valid semantic search instance with loaded index")
        return [], []
    
    return await semantic_search.search_with_scores(query, k)

# Initialize global semantic search instance
_semantic_search = None

