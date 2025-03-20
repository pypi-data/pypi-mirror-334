# pdf_signer/__init__.py
from .core import PDFSigner
from .config import SignerConfig, SignatureBoxStyle
from .exceptions import PDFSignerError, ValidationError, TagNotFoundError, SignatureDataError

__version__ = "0.1.3"
__all__ = [
    "PDFSigner", 
    "SignerConfig", 
    "SignatureBoxStyle", 
    "PDFSignerError", 
    "ValidationError", 
    "TagNotFoundError", 
    "SignatureDataError"
]