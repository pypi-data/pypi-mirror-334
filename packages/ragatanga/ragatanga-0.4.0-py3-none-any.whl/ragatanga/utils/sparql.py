"""
SPARQL query generation and validation utilities.

This module provides functions for generating SPARQL queries from natural language
and validating the syntax of SPARQL queries.
"""
# nosec B608 - This file deals with SPARQL queries, not SQL. False positive from bandit.

import json
import re
import tempfile
from typing import Any, Dict, List, Optional, Tuple, Union
import hashlib
import functools
import logging
from datetime import datetime, timedelta

from pydantic import BaseModel, Field, field_validator
from rdflib.plugins.sparql.parser import parseQuery

from ragatanga.core.llm import LLMProvider

logger = logging.getLogger(__name__)

# Cache for storing generated SPARQL queries
_SPARQL_CACHE: Dict[str, Tuple[str, datetime]] = {}
_CACHE_EXPIRY = timedelta(hours=24)  # Cache entries expire after 24 hours


def validate_sparql_query(query: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a SPARQL query for syntax correctness and compliance with owlready2's native engine.
    
    This validator checks:
    1. Basic SPARQL syntax using rdflib's parser
    2. Compatibility with owlready2's supported SPARQL subset
    
    Args:
        query: The SPARQL query to validate
        
    Returns:
        A tuple of (is_valid, error_message)
        - is_valid: Boolean indicating if the query is valid
        - error_message: Error message if query is invalid, None otherwise
    """
    # Check for basic syntax errors first
    try:
        parseQuery(query)
    except Exception as e:
        return False, f"SPARQL syntax error: {str(e)}"
    
    # Check for unsupported query types in owlready2
    query_upper = query.upper()
    
    # Check for unsupported query types
    unsupported_keywords = [
        "ASK", "DESCRIBE", "CONSTRUCT", "LOAD", "ADD", "MOVE", 
        "COPY", "CLEAR", "DROP", "INSERT DATA", "DELETE DATA", 
        "DELETE WHERE", "SERVICE", "MINUS"
    ]
    
    # Find if the query contains any unsupported keywords at the beginning of the query
    # (after potential prefix declarations)
    query_without_prefixes = re.sub(r"PREFIX\s+[^{]+", "", query_upper)
    query_type = query_without_prefixes.strip().split()[0] if query_without_prefixes.strip() else ""
    
    if query_type in unsupported_keywords:
        return False, f"Unsupported query type in owlready2: {query_type}"
    
    # Check for complex nested property paths (which owlready2 doesn't support)
    # This is a simplified check that may have false positives or negatives
    if re.search(r'\([^()]*\/[^()]*\*\)[*+]', query):  # Nested repeats like (a/p*)*
        return False, "Unsupported property path: nested repeats like (a/p*)* are not supported in owlready2"
    
    if re.search(r'\([^()]*\/[^()]*\)[*+]', query):  # Sequence in repeat like (p1/p2)*
        return False, "Unsupported property path: sequence in repeat like (p1/p2)* is not supported in owlready2"
    
    if re.search(r'\(\![^()]*\|[^()]*\)[*+]', query):  # Negative property set in repeat
        return False, "Unsupported property path: negative property set in repeat like (!(p1|p2))* is not supported in owlready2"
    
    # Check for FROM/FROM NAMED which are not supported
    if "FROM" in query_upper and (
        "FROM " in query_upper or 
        re.search(r'FROM\s+', query_upper)
    ):
        return False, "FROM keyword is not supported in owlready2's native SPARQL engine"
    
    return True, None


class SPARQLQueryPlan(BaseModel):
    """
    A Pydantic model for storing the plan-and-solve steps involved in generating
    a SPARQL query with a language model.

    Attributes:
        query_analysis: Analysis of the natural language query, identifying relevant
            ontology concepts and constraints.
        query_plan: Step-by-step plan for constructing the SPARQL query using
            ontology-specific URIs and standard SPARQL patterns.
        sparql_query: The final SPARQL query with proper PREFIX declarations and W3C
            standard syntax.
    """
    query_analysis: str = Field(
        ...,
        description="Analysis of the natural language query and identification of relevant concepts from the ontology schema."
    )
    query_plan: str = Field(
        ...,
        description="Step-by-step plan for constructing the SPARQL query using standard patterns and ontology-specific URIs."
    )
    sparql_query: str = Field(
        ...,
        description="The final SPARQL query with proper PREFIX declarations and W3C standard syntax."
    )

    @field_validator("sparql_query")
    def validate_sparql_query(cls, value: str) -> str:
        """
        Validate that the SPARQL query has proper syntax and includes
        essential PREFIX declarations. Also check for compatibility with
        owlready2's native SPARQL engine.

        Args:
            value: The SPARQL query string to validate.

        Returns:
            The validated SPARQL query, optionally with standard prefixes added.

        Raises:
            ValueError: If the SPARQL query fails syntax parsing or is not compatible
                        with owlready2's native SPARQL engine.
        """
        # Insert standard prefixes if none are present.
        if "PREFIX" not in value.upper():
            prefixes = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""
            value = prefixes + value

        # Validate using our enhanced validator
        is_valid, error_message = validate_sparql_query(value)
        if not is_valid:
            logger.warning(f"SPARQL validation failed: {error_message}")
            # Include the original query in the error message to help with debugging
            error_with_query = f"Invalid SPARQL query: {error_message}\nQuery: {value}"
            raise ValueError(error_with_query)

        return value


class SPARQLGenerator:
    """
    A class responsible for generating SPARQL queries from natural language
    using an LLM and provided ontology schemas.
    """

    def __init__(self, llm_provider: Optional[LLMProvider] = None) -> None:
        """
        Initialize the SPARQL generator.

        Args:
            llm_provider: Optional LLMProvider instance. If None, a default
                provider will be used.
        """
        self.llm_provider = llm_provider

    async def generate_query(
        self,
        query: str,
        schema_str: str,
        temperature: float = 0.2,
        llm_provider: Optional[LLMProvider] = None,
        translate_query: bool = False,
        target_language: str = "en",
        parameters: Optional[List] = None,
        **kwargs: Any
    ) -> str:
        """
        Convert a natural language query into a SPARQL query using the LLM.

        This method:
          - Optionally translates the query into the target language.
          - Constructs a system prompt with the provided ontology schema.
          - Calls the LLM to produce a structured SPARQLQueryPlan.
          - Returns the validated SPARQL query.

        Args:
            query: Natural language query in any language.
            schema_str: Ontology schema (e.g., JSON-LD, Turtle, N-Triples) as a string.
            temperature: Model temperature (lower for deterministic output).
            llm_provider: Optional override for LLMProvider instance.
            translate_query: Whether to translate the query before generating SPARQL.
            target_language: Target language code for translation (e.g., "en").
            parameters: Optional list of parameters for parameterized SPARQL queries.
            **kwargs: Additional parameters passed to the underlying LLM.

        Returns:
            A syntactically valid SPARQL query referencing the provided ontology.
        """
        provider = llm_provider or self.llm_provider or LLMProvider.get_provider()

        # Translate the input query if requested.
        translated_query = (
            await self._translate_query(query, provider, target_language)
            if translate_query
            else query
        )

        # Build the prompts (system + user).
        system_prompt = self._build_system_prompt(schema_str)
        
        # Adjust the user message to mention parameterization if parameters are provided
        param_hint = ""
        if parameters is not None and len(parameters) > 0:
            param_types = [type(p).__name__ for p in parameters]
            param_hint = f"\n\nPlease use parameterized queries with ?? syntax for these dynamic values: {param_types}"
            
        user_message = (
            f"Question: {translated_query}{param_hint}\n\n"
            f"Please analyze this question and generate a SPARQL query that retrieves "
            f"the relevant information from the ontology described in the system prompt."
        )

        # Call the LLM to generate a structured SPARQLQueryPlan.
        try:
            structured_response = await provider.generate_structured(
                prompt=user_message,
                response_model=SPARQLQueryPlan,
                system_prompt=system_prompt,
                temperature=temperature,
                **kwargs
            )
            
            # Return the SPARQL query (validation is handled by the SPARQLQueryPlan model)
            return structured_response.sparql_query
            
        except Exception as exc:
            logger.error(f"Error generating SPARQL query with LLM: {exc}")
            raise

    def _build_system_prompt(self, schema_str: str) -> str:
        """
        Construct the system prompt with ontology schema details and guidelines
        for generating SPARQL queries.

        Args:
            schema_str: String representation of the ontology schema.

        Returns:
            A system prompt string instructing the LLM on how to build SPARQL queries.
        """
        # Sanitize the schema string to prevent injection attacks
        # Remove any characters that could be used for prompt injection
        def sanitize_schema(schema: str) -> str:
            # Remove potentially dangerous characters or sequences
            # This is a basic sanitization - adjust based on your specific needs
            if not schema:
                return "No schema available"
                
            # Replace backticks which could break out of code blocks
            schema = schema.replace("`", "'")
            
            # Replace any triple backticks which could break out of code blocks
            schema = schema.replace("```", "'''")
            
            # Limit length to prevent excessive output
            max_length = 5000
            if len(schema) > max_length:
                schema = schema[:max_length] + "... [truncated for length]"
                
            return schema
            
        # Apply sanitization
        safe_schema = sanitize_schema(schema_str)
        
        # This is a SPARQL prompt template, not SQL - bandit is giving a false positive
        # The schema_str is sanitized above to prevent any injection
        prompt = (  # nosec B608
            "You are a SPARQL query expert specializing in ontology querying with owlready2.\n"
            "Your task is to translate natural language questions into precise SPARQL queries "
            "that work with owlready2's native SPARQL engine, which has high performance but "
            "supports only a subset of the SPARQL standard.\n\n"
            "IMPORTANT GUIDELINES:\n"
            "1. Always include necessary PREFIX declarations based on the provided ontology\n"
            "2. Use DISTINCT to avoid duplicate results\n"
            "3. Include rdfs:label when available for human-readable results\n"
            "4. Use OPTIONAL for potentially missing properties\n"
            "5. Include FILTER when appropriate to narrow results by language, type, or value constraints\n"
            "6. Use LIMIT as needed for controlling result size\n"
            "7. Make extensive use of property path expressions to simplify queries:\n"
            "   - Use rdf:type/rdfs:subClassOf* to find instances of a class or any of its subclasses\n"
            "   - Use rdfs:subClassOf+ to find all superclasses (excluding the class itself)\n"
            "   - Use rdfs:subClassOf* to find all superclasses (including the class itself)\n"
            "   - Use property* for zero or more occurrences of a property\n"
            "   - Use property+ for one or more occurrences of a property\n"
            "   - Use property? for zero or one occurrence of a property\n"
            "   - Use property1/property2 for property chains (property1 followed by property2)\n"
            "   - Use ^property for inverse property traversal\n"
            "8. For dynamic values that might be provided later, use parameterized queries with the ?? syntax\n"
            "   Example: 'SELECT ?x WHERE { ?x rdfs:label ?? }' where ?? will be replaced by a parameter\n"
            "   You can also use numbered parameters like ??1, ??2 for multiple occurrences\n\n"
            "OWLREADY2 SPARQL LIMITATIONS (AVOID THESE):\n"
            "1. Do NOT use ASK, DESCRIBE, LOAD, ADD, MOVE, COPY, CLEAR, DROP, or CONSTRUCT queries\n"
            "2. Do NOT use INSERT DATA, DELETE DATA, or DELETE WHERE (use INSERT or DELETE instead)\n"
            "3. Do NOT use SERVICE (federated queries)\n"
            "4. Do NOT use FROM or FROM NAMED keywords\n"
            "5. Do NOT use MINUS\n"
            "6. Do NOT use complex property paths with nested repeats or sequences in repeats:\n"
            "   - Avoid patterns like (a/p*)* (nested repeats)\n"
            "   - Avoid patterns like (p1/p2)* (sequence in repeat)\n"
            "   - Avoid patterns like (!(p1|p2))* (negative property set in repeat)\n\n"
            "OWLREADY2 SPARQL EXTENSIONS (USEFUL):\n"
            "1. SIMPLEREPLACE(a, b) - faster non-regex version of REPLACE()\n"
            "2. LIKE(a, b) - SQL-like pattern matching, faster than regex\n"
            "3. NEWINSTANCEIRI(class) - create a new IRI for a new instance\n"
            "4. LOADED(iri) - check if entity is loaded in Python\n"
            "5. DATE(), TIME(), DATETIME() - date/time functions\n"
            "6. DATE_ADD(), DATE_SUB(), DATETIME_ADD(), DATETIME_SUB() - date arithmetic\n\n"
            f"ONTOLOGY SCHEMA:\nThe following schema shows the classes and properties "
            f"available in the ontology:\n\n{safe_schema}\n\n"
            "GENERIC SPARQL PATTERNS:\n"
            "1. Finding instances of a class and all its subclasses:\n"
            "```\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"
            "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
            "PREFIX owl: <http://www.w3.org/2002/07/owl#>\n"
            "PREFIX : <http://example.org/ontology#>\n\n"
            "SELECT DISTINCT ?instance ?label\n"
            "WHERE {\n"
            "  ?instance rdf:type/rdfs:subClassOf* :ClassName ;\n"
            "            rdfs:label ?label .\n"
            "}\n```\n\n"
            "2. Finding instances with specific property values:\n"
            "```\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"
            "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
            "PREFIX : <http://example.org/ontology#>\n\n"
            "SELECT DISTINCT ?instance ?label ?relatedValue\n"
            "WHERE {\n"
            "  ?instance rdf:type/rdfs:subClassOf* :ClassName ;\n"
            "            rdfs:label ?label ;\n"
            '            :someProperty "Some Value" .\n'
            "  OPTIONAL { ?instance :anotherProperty ?relatedValue }\n"
            "}\n```\n\n"
            "3. Finding relationships between instances:\n"
            "```\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"
            "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
            "PREFIX : <http://example.org/ontology#>\n\n"
            "SELECT DISTINCT ?instance1 ?label1 ?instance2 ?label2\n"
            "WHERE {\n"
            "  ?instance1 rdf:type/rdfs:subClassOf* :Class1 ;\n"
            "             rdfs:label ?label1 ;\n"
            "             :relatesTo ?instance2 .\n"
            "  ?instance2 rdf:type/rdfs:subClassOf* :Class2 ;\n"
            "             rdfs:label ?label2 .\n"
            "}\n```\n\n"
            "4. Using parameterized queries for dynamic values:\n"
            "```\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"
            "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
            "PREFIX : <http://example.org/ontology#>\n\n"
            "SELECT DISTINCT ?instance ?label\n"
            "WHERE {\n"
            "  ?instance rdf:type/rdfs:subClassOf* :ClassName ;\n"
            "            rdfs:label ?label ;\n"
            "            :someProperty ?? .\n"
            "}\n```\n\n"
            "5. Using property path expressions for complex relationships:\n"
            "```\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"
            "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
            "PREFIX owl: <http://www.w3.org/2002/07/owl#>\n"
            "PREFIX : <http://example.org/ontology#>\n\n"
            "SELECT DISTINCT ?instance ?superClass\n"
            "WHERE {\n"
            "  ?instance rdf:type :ClassName .\n"
            "  :ClassName rdfs:subClassOf+ ?superClass .\n"
            "}\n```\n\n"
            "6. Finding all paths between two entities (with bounded length):\n"
            "```\nPREFIX : <http://example.org/ontology#>\n\n"
            "SELECT DISTINCT ?intermediateNode\n"
            "WHERE {\n"
            "  :StartNode (:property1|:property2|:property3)+ ?intermediateNode .\n"
            "  ?intermediateNode (:property1|:property2|:property3)* :EndNode .\n"
            "}\n```\n\n"
            "7. Creating new data with INSERT (supported in owlready2):\n"
            "```\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"
            "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
            "PREFIX owl: <http://www.w3.org/2002/07/owl#>\n"
            "PREFIX : <http://example.org/ontology#>\n\n"
            "INSERT { \n"
            "  ?x rdfs:label \"New label\"@en \n"
            "}\n"
            "WHERE { \n"
            "  ?x rdf:type :SpecificClass \n"
            "}\n```\n\n"
            "Now, generate a valid SPARQL query for the user's question, based on the ontology above."
        )
        return prompt

    async def _translate_query(
        self, query: str, provider: LLMProvider, target_language: str
    ) -> str:
        """
        Translate the query into the target language using the LLM provider.

        Args:
            query: Original natural language query.
            provider: LLMProvider instance to handle translation.
            target_language: The language code to translate the query into.

        Returns:
            The translated query, or the original if translation fails.
        """
        # To avoid circular imports, import here only if needed.
        from ragatanga.utils.translation import translate_query_to_ontology_language

        try:
            translated_query = await translate_query_to_ontology_language(
                query=query,
                target_language=target_language,
                llm_provider=provider
            )
            if translated_query != query:
                logger.info(f"Translated query from '{query}' to '{translated_query}'")
            return translated_query
        except Exception as exc:
            logger.warning(f"Translation failed; using original query. Error: {exc}")
            return query


def _generate_cache_key(query: str, schema_str: str, parameters: Optional[List] = None) -> str:
    """
    Generate a cache key for a SPARQL query generation request.
    
    Args:
        query: The natural language query.
        schema_str: The ontology schema.
        parameters: Optional parameters for the query.
        
    Returns:
        A string hash that can be used as a cache key.
    """
    # Normalize the query by removing extra whitespace and converting to lowercase
    normalized_query = re.sub(r'\s+', ' ', query.strip().lower())
    
    # Create a hash of the schema to avoid storing the full schema in the key
    schema_hash = hashlib.md5(schema_str.encode()).hexdigest()
    
    # Include parameters in the key if provided
    param_str = ""
    if parameters:
        param_str = json.dumps(parameters, sort_keys=True)
    
    # Combine all components and hash
    combined = f"{normalized_query}|{schema_hash}|{param_str}"
    return hashlib.md5(combined.encode()).hexdigest()


async def generate_sparql_query(
    query: str,
    schema_str: str,
    llm_provider: Optional[LLMProvider] = None,
    temperature: float = 0.2,
    translate_query: bool = False,
    target_language: str = "en",
    parameters: Optional[List] = None,
    use_cache: bool = True,
    **kwargs: Any
) -> str:
    """
    Public utility function for generating a SPARQL query from a natural language prompt
    and an ontology schema.

    Args:
        query: Natural language query string.
        schema_str: Ontology schema in any supported format (e.g., JSON-LD, Turtle).
        llm_provider: Optional LLMProvider override.
        temperature: Model temperature for LLM outputs.
        translate_query: Whether to translate the query to the target language.
        target_language: Language code if translation is enabled.
        parameters: Optional list of parameters for parameterized SPARQL queries.
        use_cache: Whether to use the query cache (default: True).
        **kwargs: Additional keyword arguments for the LLM.

    Returns:
        A syntactically valid SPARQL query string referencing the provided ontology schema.

    Example:
        >>> query = "What are all the classes in the ontology?"
        >>> schema = "... (some Turtle or JSON-LD data) ..."
        >>> sparql_query = await generate_sparql_query(query, schema)
        >>> print(sparql_query)
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        ...
        SELECT DISTINCT ?class ?label
        WHERE {
          ?class a rdfs:Class .
          OPTIONAL { ?class rdfs:label ?label }
        }
    """
    # Check cache first if enabled
    if use_cache:
        cache_key = _generate_cache_key(query, schema_str, parameters)
        cached_result = _SPARQL_CACHE.get(cache_key)
        
        if cached_result:
            sparql_query, timestamp = cached_result
            # Check if the cache entry is still valid
            if datetime.now() - timestamp < _CACHE_EXPIRY:
                logger.debug(f"Using cached SPARQL query for: {query}")
                return sparql_query
            else:
                # Remove expired cache entry
                del _SPARQL_CACHE[cache_key]
    
    # Generate the query if not in cache or cache is disabled
    generator = SPARQLGenerator(llm_provider)
    sparql_query = await generator.generate_query(
        query=query,
        schema_str=schema_str,
        temperature=temperature,
        translate_query=translate_query,
        target_language=target_language,
        parameters=parameters,
        **kwargs
    )
    
    # Store in cache if enabled
    if use_cache:
        _SPARQL_CACHE[cache_key] = (sparql_query, datetime.now())
        
        # Clean up old cache entries if cache is getting large
        if len(_SPARQL_CACHE) > 1000:  # Arbitrary limit to prevent memory issues
            current_time = datetime.now()
            expired_keys = [
                k for k, (_, t) in _SPARQL_CACHE.items() 
                if current_time - t >= _CACHE_EXPIRY
            ]
            for k in expired_keys:
                del _SPARQL_CACHE[k]
    
    return sparql_query


async def generate_sparql_for_query(self, query: str, schema: Dict[str, Any]) -> str:
    """Generate a SPARQL query from a natural language question and a schema dict."""
    from ragatanga.utils.sparql import generate_sparql_query
    schema_str = json.dumps(schema, indent=2)
    logger.info(f"Schema: {schema_str}")
    # remove all individuals from the schema
    schema_str = re.sub(r':\w+ rdf:type owl:NamedIndividual,', '', schema_str)
    
    # Debug logging
    logger.debug(f"Schema size: {len(schema_str)} bytes")
    logger.debug(f"Schema classes: {len(schema['classes'])} classes")
    logger.debug(f"Schema properties: {len(schema['properties'])} properties")
    logger.debug(f"Schema individuals: {len(schema.get('individuals', {}))} individuals")
    
    # Sample of the classes and properties
    class_sample = list(schema['classes'].keys())[:5]
    prop_sample = list(schema['properties'].keys())[:5]
    logger.debug(f"Sample classes: {class_sample}")
    logger.debug(f"Sample properties: {prop_sample}")
    
    # Write schema to file for inspection using a secure temp file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_file.write(schema_str)
        logger.debug(f"Schema written to temporary file: {temp_file.name}")
            
    return await generate_sparql_query(query, schema_str)


def extract_parameters(query: str) -> List[str]:
    """
    Extract parameter names from a parameterized query string.
    
    Parameters are expected to be in the format {parameter_name}.
    
    Args:
        query: The query string containing parameters in curly braces
        
    Returns:
        A list of parameter names found in the query
    """
    # Use regex to find all parameters in the format {parameter_name}
    pattern = r'\{([a-zA-Z0-9_]+)\}'
    matches = re.findall(pattern, query)
    return matches
