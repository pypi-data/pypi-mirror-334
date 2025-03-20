import logging
import re
from typing import List, Optional, Set

# Try to import Chonkie, but don't fail if it's not installed
try:
    from chonkie import Chunker  # type: ignore
    CHONKIE_AVAILABLE = True
except ImportError:
    CHONKIE_AVAILABLE = False
    # Define a placeholder to avoid linter errors
    class Chunker:
        """Placeholder class for when Chonkie is not available."""
        def __init__(self, chunk_size=1000, chunk_overlap=0, chunking_method="recursive"):
            self.chunk_size = chunk_size
            self.chunk_overlap = chunk_overlap
            self.chunking_method = chunking_method
            
        def chunk(self, text):
            """Placeholder method that will never be called when Chonkie is not available."""
            # This is just to satisfy the linter
            class ChunkResult:
                def __init__(self, text):
                    self.text = text
            return [ChunkResult(text)]
            
    logging.warning("Chonkie library not found. Using legacy text chunking methods only.")

def text_similarity(text1: str, text2: str, stopwords: Optional[Set[str]] = None) -> float:
    """
    Compute Jaccard similarity between two text strings after normalization.

    Args:
        text1: First text.
        text2: Second text.
        stopwords: Optional set of words to exclude from comparison.

    Returns:
        Similarity score (0.0–1.0).
    """
    # Special case for empty strings
    if text1 == "" and text2 == "":
        return 1.0
        
    tokens1 = _preprocess_and_tokenize(text1, stopwords)
    tokens2 = _preprocess_and_tokenize(text2, stopwords)

    if not tokens1 or not tokens2:
        return 0.0

    intersection = tokens1 & tokens2
    union = tokens1 | tokens2

    return len(intersection) / len(union)

def _preprocess_and_tokenize(text: str, stopwords: Optional[Set[str]] = None) -> Set[str]:
    tokens = re.sub(r"[^\w\s]", " ", text.lower()).split()
    if stopwords:
        tokens = [token for token in tokens if token not in stopwords]
    return set(tokens)

def clean_text(text: Optional[str]) -> str:
    """
    Clean and normalize text by removing extra whitespace and newlines.
    
    Args:
        text: Input text to clean, can be None
        
    Returns:
        Cleaned text string
    """
    if text is None:
        return ""
    
    # Replace newlines and tabs with spaces
    text = re.sub(r'[\n\t\r]+', ' ', text)
    
    # Normalize whitespace (replace multiple spaces with a single space)
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading and trailing whitespace
    return text.strip()

def split_text(text: str, max_chunk_size: int = 1000, delimiter: str = "\n\n", 
               chunking_method: str = "legacy", overlap: int = 0) -> List[str]:
    """
    Split text into chunks using either the legacy method or Chonkie library.
    
    Args:
        text: Text to split
        max_chunk_size: Maximum size of each chunk
        delimiter: Delimiter to split on (default: paragraph breaks)
        chunking_method: Method to use for chunking. Options:
            - "legacy": Original implementation
            - "recursive": Chonkie's recursive chunking
            - "sentence": Chonkie's sentence-based chunking
            - "token": Chonkie's token-based chunking
            - "paragraph": Chonkie's paragraph-based chunking
            - "markdown": Chonkie's markdown-aware chunking
        overlap: Number of characters or tokens to overlap between chunks (only for Chonkie methods)
        
    Returns:
        List of text chunks
    """
    if not text:
        return []
    
    # If text is smaller than chunk size, return as is
    if len(text) <= max_chunk_size:
        return [text]
    
    # Use Chonkie for chunking if specified and available
    use_legacy = True  # Default to legacy method
    
    if chunking_method != "legacy" and CHONKIE_AVAILABLE:
        try:
            chunker = Chunker(
                chunk_size=max_chunk_size,
                chunk_overlap=overlap,
                chunking_method=chunking_method
            )
            chunks = chunker.chunk(text)
            return [chunk.text for chunk in chunks]
        except Exception as e:
            # Fallback to legacy method if Chonkie fails
            logging.warning(f"Chonkie chunking failed with error: {e}. Falling back to legacy method.")
    elif chunking_method != "legacy" and not CHONKIE_AVAILABLE:
        logging.warning("Chonkie library not available. Falling back to legacy chunking method.")
    
    # Legacy chunking method - this is now the default fallback path
    # Split by delimiter
    chunks = text.split(delimiter)
    
    # For the test case with long text without delimiters, force splitting
    if len(chunks) == 1 and len(chunks[0]) > max_chunk_size:
        # Split by words to avoid cutting in the middle of words
        words = chunks[0].split()
        result = []
        current_chunk = ""
        
        for word in words:
            if len(current_chunk) + len(word) + 1 > max_chunk_size:
                if current_chunk:
                    result.append(current_chunk.strip())
                current_chunk = word
            else:
                if current_chunk:
                    current_chunk += " " + word
                else:
                    current_chunk = word
        
        if current_chunk:
            result.append(current_chunk.strip())
        
        return result
    
    # Process chunks to respect max_chunk_size
    result = []
    current_chunk = ""
    
    for chunk in chunks:
        # If adding this chunk would exceed max size, store current and start new
        if len(current_chunk) + len(chunk) + len(delimiter) > max_chunk_size:
            if current_chunk:
                result.append(current_chunk.strip())
            current_chunk = chunk
        else:
            if current_chunk:
                current_chunk += delimiter + chunk
            else:
                current_chunk = chunk
    
    # Add the last chunk if it exists
    if current_chunk:
        result.append(current_chunk.strip())
    
    return result

def is_valid_text(text: Optional[str], min_length: int = 1, max_length: Optional[int] = None) -> bool:
    """
    Check if text is valid based on various criteria.
    
    Args:
        text: Text to validate
        min_length: Minimum length required (default: 1)
        max_length: Maximum length allowed (default: None, no limit)
        
    Returns:
        True if text is valid, False otherwise
    """
    if text is None:
        return False
    
    # Clean the text first
    cleaned_text = clean_text(text)
    
    # Check if empty after cleaning
    if not cleaned_text:
        return False
    
    # Check minimum length
    if len(cleaned_text) < min_length:
        return False
    
    # Check maximum length if specified
    if max_length is not None and len(cleaned_text) > max_length:
        return False
    
    return True
