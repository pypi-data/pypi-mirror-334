"""
Custom exceptions for Ragatanga.
"""

class ConfigurationError(Exception):
    """Exception raised when there's a configuration error."""
    
    def __init__(self, message: str, detailed_message: str | None = None, error_code: str | None = None):
        """
        Initialize the exception.
        
        Args:
            message: Short error message
            detailed_message: More detailed explanation 
            error_code: Error code for identification
        """
        self.message = message
        self.detailed_message = detailed_message or message
        self.error_code = error_code or "configuration_error"
        super().__init__(self.message) 