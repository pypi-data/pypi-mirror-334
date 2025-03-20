"""
Query generation and processing module for Ragatanga.

This module handles query analysis, processing, and answer generation.
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field
from loguru import logger

from ragatanga.core.llm import LLMProvider
from ragatanga.core.models import QueryResponse, RetrievedData, EntityInfo

async def analyze_query_type(query: str, llm_provider=None) -> str:
    """
    Analyze the query to determine its type for better answer generation.
    
    Args:
        query: The query string
        llm_provider: LLM provider to use (if None, uses default)
        
    Returns:
        Query type: 'factual', 'descriptive', 'comparative', 'procedural', or 'exploratory'
    """
    if llm_provider is None:
        llm_provider = LLMProvider.get_provider()
    
    system_prompt = """
    You are a query analysis expert. Determine the type of the given query.
    Categorize it as one of the following:
    
    - factual: Simple questions asking for specific facts (e.g., "What is the price of Plan X?")
    - descriptive: Questions asking for descriptions (e.g., "Tell me about the São Bento unit")
    - comparative: Questions asking for comparisons (e.g., "What's the difference between Plan X and Plan Y?")
    - procedural: Questions about how to do something (e.g., "How do I cancel my subscription?")
    - exploratory: Open-ended questions seeking broader information (e.g., "What services are available?")
    
    Return only the category name, nothing else.
    """
    
    try:
        response = await llm_provider.generate_text(
            prompt=query,
            system_prompt=system_prompt,
            temperature=0.0,  # Use deterministic output
            max_tokens=50     # Very short response needed
        )
        
        query_type = response.strip().lower()
        
        # Validate and default to 'factual' if not recognized
        valid_types = {'factual', 'descriptive', 'comparative', 'procedural', 'exploratory'}
        if query_type not in valid_types:
            return 'factual'
            
        return query_type
    except Exception as e:
        logger.error(f"Error analyzing query type: {str(e)}")
        # Default to factual if analysis fails
        return 'factual'

def generate_system_prompt_by_query_type(query_type: str) -> str:
    """
    Generate a system prompt tailored to the query type.
    
    Args:
        query_type: Type of the query
        
    Returns:
        System prompt for the LLM
    """
    base_prompt = """
    You are an intelligent assistant specializing in ontology and knowledge retrieval system information.
    Your task is to provide accurate, objective answers based on the provided facts.
    
    IMPORTANT GUIDELINES:
    1. Focus primarily on high-confidence facts
    2. When facts from different sources conflict, prefer SPARQL results over semantic search
    3. Be concise and factual - avoid unnecessary verbosity
    4. Structure your responses clearly and directly
    5. Return exact counts and lists when relevant (e.g., number of components, systems, etc.)
    6. Only include information that is directly relevant to the query

    RESPONSE STRUCTURE REQUIREMENTS:
    - The 'answer' field should contain a brief, factual response to the user's query
    - If the query is about counts or lists, provide those numbers and items explicitly
    - The 'full_answer' field should contain a more comprehensive response
    - The 'number_of_systems' field should contain the exact count of systems/components when relevant
    - The 'list_of_systems' field should contain the names of those systems/components
    """
    
    if query_type == "factual":
        # For factual queries, emphasize precision and conciseness
        additional_instructions = """
        For this factual query:
        - Provide exact numbers, names, and details
        - Avoid speculation or elaboration
        - Structure your response in a clear, factual format
        - Prioritize SPARQL results as they contain structured data
        """
    elif query_type == "descriptive":
        # For descriptive queries, allow more comprehensive explanation
        additional_instructions = """
        For this descriptive query:
        - Provide a clear, objective description
        - Include key details while avoiding excessive verbosity
        - Organize information in a logical structure
        - Balance SPARQL and semantic search results appropriately
        """
    elif query_type == "comparative":
        # For comparative queries, emphasize structure and clarity
        additional_instructions = """
        For this comparative query:
        - Clearly identify the items being compared
        - Present similarities and differences in an organized way
        - Use factual comparisons rather than evaluative language
        - Present information in a structured format
        """
    elif query_type == "exploratory":
        # For exploratory queries, provide comprehensive but organized information
        additional_instructions = """
        For this exploratory query:
        - Present the most important facts first
        - Organize information logically
        - Include diverse relevant information while maintaining focus
        - Balance breadth and depth appropriately
        """
    else:
        # Default instructions for other query types
        additional_instructions = """
        For this query:
        - Focus on providing direct, factual information
        - Structure your response clearly
        - Prioritize clarity and accuracy
        """
    
    return base_prompt + additional_instructions

def generate_fallback_answer(query: str, sparql_facts: List[str], semantic_facts: List[str]) -> str:
    """
    Generate a simple fallback answer when LLM generation fails.
    
    Args:
        query: The user's query
        sparql_facts: Facts from SPARQL queries
        semantic_facts: Facts from semantic search
        
    Returns:
        A simple answer based on the facts
    """
    # Combine all facts
    all_facts = sparql_facts + semantic_facts
    
    if not all_facts:
        return f"I don't have enough information to answer the question: '{query}'. Please try a different query."
    
    # Create a simple answer
    answer = f"Here's what I found about '{query}':\n\n"
    
    # Add SPARQL facts
    if sparql_facts:
        answer += "From structured data:\n"
        for i, fact in enumerate(sparql_facts):
            answer += f"- {fact}\n"
        answer += "\n"
    
    # Add semantic facts
    if semantic_facts:
        answer += "From unstructured data:\n"
        for i, fact in enumerate(semantic_facts):
            answer += f"- {fact}\n"
        answer += "\n"
    
    answer += "This is a fallback answer generated from the available facts."
    
    return answer

class QueryAnalysisResponse(BaseModel):
    """
    Structured response for query analysis and system prompt generation.
    
    This model combines the query type analysis and system prompt generation
    into a single structured output from the LLM. The query type helps identify
    what kind of information the user is seeking, while the system prompt guides
    the LLM in generating an appropriate response.
    """
    inferred_query_type: str = Field(
        ..., 
        description="""
        The inferred type of the query. Choose from one of the following categories:
        - 'factual': Questions seeking specific facts, e.g. "What is X?" or "How does Y work?"
        - 'comparative': Questions comparing multiple entities, e.g. "What's the difference between X and Y?"
        - 'exploratory': Open-ended questions seeking broader information, e.g. "Tell me about X"
        - 'procedural': Questions about how to do something, e.g. "How do I X?"
        - 'causal': Questions about cause and effect, e.g. "Why does X happen?"
        - 'analytical': Questions requiring interpretation or analysis, e.g. "What are the implications of X?"
        - 'quantitative': Questions about quantities or measurements, e.g. "How many X are there?"
        - 'definitional': Questions seeking definitions, e.g. "What is the definition of X?"
        - 'temporal': Questions about time or timelines, e.g. "When did X happen?"
        - 'conditional': Questions about what would happen if certain conditions were met, e.g. "What if X?"
        - 'other': For queries that don't fit other categories
        """
    )
    
    generated_system_prompt: str = Field(
        ...,
        description="""
        A system prompt tailored to the query type that will guide the LLM in generating an appropriate response.
        The system prompt should:
        - Set the appropriate tone and style for the query type
        - Guide the LLM to focus on the most relevant aspects of the retrieved information
        - Encourage clear, concise, and accurate responses
        - Include instructions for handling uncertain or missing information
        - Adapt to the complexity and specificity of the query
        """
    )
    
    model_config = {"validate_assignment": True}

async def analyze_query_and_generate_prompt(query: str, llm_provider=None) -> QueryAnalysisResponse:
    """
    Analyze a query and generate an appropriate system prompt in a single LLM call.
    
    Args:
        query: The user's query
        llm_provider: LLM provider to use (if None, uses default)
        
    Returns:
        QueryAnalysisResponse with inferred query type and generated system prompt
    """
    if llm_provider is None:
        llm_provider = LLMProvider.get_provider()
    
    system_prompt = """You are an AI assistant specialized in analyzing queries and generating appropriate system prompts.
Your task is to:
1. Determine the type of query being asked
2. Generate an appropriate system prompt that will guide an LLM in answering the query effectively
Be specific and detailed in your analysis."""
    
    user_prompt = f"""Analyze the following query and generate an appropriate system prompt:

Query: "{query}"

Please classify this query by type and generate a custom system prompt that will help an LLM provide the best possible answer."""

    try:
        return await llm_provider.generate_structured(
            prompt=user_prompt,
            system_prompt=system_prompt,
            response_model=QueryAnalysisResponse,
            temperature=0.3
        )
    except Exception as e:
        logger.error(f"Error generating structured query analysis: {str(e)}")
        # Return a default analysis if the structured generation fails
        return QueryAnalysisResponse(
            inferred_query_type="factual",
            generated_system_prompt="""You are an AI assistant that provides clear, accurate, and informative answers based on the provided information.
Focus on answering the user's query using only the provided context. If the context doesn't contain relevant information, acknowledge this limitation.
Structure your answer to be comprehensive and well-organized, with a clear introduction and conclusion when appropriate."""
        )

async def generate_structured_answer(
    query: str,
    sparql_results: List[str],
    semantic_results: List[str],
    llm_provider=None,
    temperature: float = 0.7,
    max_tokens: int = 8000
) -> QueryResponse:
    """
    Generate a structured, comprehensive answer using retrieved query results.
    
    Args:
        query: The user's query
        sparql_results: List of results retrieved from SPARQL queries
        semantic_results: List of results retrieved from semantic search
        llm_provider: LLM provider to use (if None, uses default)
        temperature: Temperature for text generation
        max_tokens: Maximum tokens for the answer
        
    Returns:
        A QueryResponse object with the structured answer
    """
    if llm_provider is None:
        llm_provider = LLMProvider.get_provider()
    
    # Initialize response components
    retrieval_data = RetrievedData(
        sparql=sparql_results,
        semantic=semantic_results
    )
    
    # Initialize empty dictionaries for entity information and metadata
    entity_info = EntityInfo()
    metadata = {}
    structured_data: Dict[str, Any] = {}
    
    # If we don't have any results, generate a fallback answer
    if not sparql_results and not semantic_results:
        logger.warning("No retrieved results, generating fallback answer")
        answer = "I apologize, but I couldn't find relevant information to answer your question."
        return QueryResponse(
            answer=answer,
            retrieval=retrieval_data,
            entities=entity_info,
            structured_data={"error": "no_results"},
            metadata={"success": False}
        )
    
    # Analyze query and generate appropriate system prompt
    query_analysis = await analyze_query_and_generate_prompt(query, llm_provider)
    logger.info(f"Query type: {query_analysis.inferred_query_type}")
    
    # Store query type in metadata
    metadata["query_type"] = query_analysis.inferred_query_type
    
    # Prepare context for prompt
    sparql_context = "\n".join([f"- {result}" for result in sparql_results]) if sparql_results else "No SPARQL results found."
    semantic_context = "\n".join([f"- {result}" for result in semantic_results]) if semantic_results else "No semantic results found."
    
    # Use the generated system prompt
    system_prompt = query_analysis.generated_system_prompt
    
    # Combine all relevant context
    context = f"""
SPARQL Results:
{sparql_context}

Semantic Results:
{semantic_context}
"""
    
    # Build the user prompt
    user_prompt = f"""
Query: {query}

Context Information:
{context}

Based on the above context, provide a comprehensive answer to the query.
"""
    
    try:
        # Generate the answer using the LLM
        logger.debug(f"Generating answer with {len(sparql_results)} SPARQL results and {len(semantic_results)} semantic results for query type {query_analysis.inferred_query_type}")
        answer = await llm_provider.generate_text(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        logger.info(f"Generated answer of length {len(answer)} chars")
        
        # Create response
        return QueryResponse(
            answer=answer,
            retrieval=retrieval_data,
            entities=entity_info,
            structured_data=structured_data,
            metadata=metadata
        )
        
    except Exception as e:
        logger.error(f"Error generating answer: {str(e)}")
        error_answer = "I apologize, but I'm having trouble generating an answer at the moment."
        
        return QueryResponse(
            answer=error_answer,
            retrieval=retrieval_data,
            entities=entity_info,
            structured_data={"error": str(e)},
            metadata={"success": False, "error": str(e)}
        )