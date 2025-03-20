# pdf_signer/utils.py
from typing import Dict, List, Tuple, Optional, Pattern, Any
import re

def create_regex_pattern(patterns: List[str]) -> Pattern:
    """Create a regex pattern from a list of tag patterns"""
    pattern_str = "|".join([f"({p})" for p in patterns])
    return re.compile(pattern_str)

def get_field_components(tag: str, pattern: Pattern) -> Tuple[str, str]:
    """Extract components from a tag based on a pattern"""
    match = pattern.match(tag)
    if match:
        groups = match.groups()
        return groups[0], groups[1] if len(groups) > 1 else ""
    return tag, ""

# pdf_signer/exceptions.py
class PDFSignerError(Exception):
    """Base exception for PDF Signer library"""
    pass

class ValidationError(PDFSignerError):
    """Raised when input validation fails"""
    pass

class TagNotFoundError(PDFSignerError):
    """Raised when no tags are found in the PDF"""
    pass

class SignatureDataError(PDFSignerError):
    """Raised when signature data is invalid"""
    pass