from loguru import logger
from pydantic import BaseModel, Field
from typing import Optional

from ragatanga.core.llm import LLMProvider

class TranslationResponse(BaseModel):
    original_query: str = Field(description="The original query")
    translated_query: str = Field(description="The translated query, must keep the same meaning/intent as the original query")

async def translate_query_to_ontology_language(
    query: str, 
    target_language: str = "en",
    llm_provider: Optional[LLMProvider] = None
) -> str:
    """
    Translates the input query to the ontology's language if needed.
    Uses simple detection by checking for non-English characters.
    
    Args:
        query: The query text to translate
        target_language: Target language code (default: "en" for English)
        llm_provider: Optional LLM provider to use for translation
        
    Returns:
        Translated query or original query if translation wasn't needed/failed
    """
    # Simple language detection (not accurate but doesn't require dependencies)
    english_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,?!-_() ")
    non_english_chars = [c for c in query if c not in english_chars]
    detected_non_english = len(non_english_chars) > 0
    
    # If we detect non-English characters, use LLM for translation
    if detected_non_english:
        logger.info(f"Detected non-English characters in query: {non_english_chars}. Translating...")
        try:
            return await translate_with_llm(query, target_language, llm_provider)
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}. Returning original query.")
            return query
    return query

async def translate_with_llm(
    query: str, 
    target_language: str = "en", 
    llm_provider: Optional[LLMProvider] = None
) -> str:
    """
    Translate text using a language model.
    
    Args:
        query: Text to translate
        target_language: Target language code
        llm_provider: Optional LLM provider to use
        
    Returns:
        Translated text or original if translation failed
    """
    try:
        # Use provided LLM provider or get default
        provider = llm_provider
        if provider is None:
            provider = LLMProvider.get_provider()
        
        system_prompt = f"You are a translator. Translate the following text to {target_language} only. Return only the translation, no explanations or additional text."
        
        translated = await provider.generate_structured(
            prompt=query,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=1000,
            response_model=TranslationResponse
        )
        
        return translated.translated_query if translated else query
    except Exception as e:
        logger.error(f"LLM translation failed: {str(e)}. Returning original query.")
        return query
