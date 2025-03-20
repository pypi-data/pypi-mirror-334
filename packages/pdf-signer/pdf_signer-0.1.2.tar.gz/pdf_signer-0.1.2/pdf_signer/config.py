# pdf_signer/config.py
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Pattern, Any
import re
from functools import partial

@dataclass
class SignatureBoxStyle:
    """Configuration for signature box appearance"""
    # Box dimensions
    box_width: float = 28
    box_height: float = 27
    
    # Colors (RGB format)
    background_color: Tuple[float, float, float] = (0.8039, 0.8549, 0.9922)  # Light blue
    text_color: Tuple[float, float, float] = (0, 0, 0)  # Black
    border_color: Tuple[float, float, float] = (0, 0, 0)  # Black
    
    # Border style
    border_width: float = 0.5
    border_style: str = "dotted"  # Options: "solid", "dotted", "dashed"
    
    # Font settings
    name_font: str = "Helvetica-Bold"
    name_font_size_factor: float = 0.45  # Percentage of box height
    max_name_font_size: float = 7
    
    meta_font: str = "Helvetica"
    meta_font_size_factor: float = 0.3  # Percentage of box height
    max_meta_font_size: float = 6
    
    # Row configuration
    row_data: List[str] = field(default_factory=lambda: ["name", "Digitally signed at:", "IP", "Date"])
    
    # Tick image
    tick_image_size_factor: float = 0.4  # Percentage of box height
    tick_image_position: Tuple[float, float] = (0.8, 0.5)  # Relative position (x, y) in box


def default_pattern():
    return re.compile(r"(int_p|count_p)(\d+)")


def default_style_overrides():
    return {}


@dataclass
class SignerConfig:
    """Main configuration for PDF signer"""
    # Tag pattern configuration
    tag_pattern: Pattern = field(default_factory=default_pattern)
    tag_pattern_str: str = r"(int_p|count_p)(\d+)"
    
    # Default box style
    default_style: SignatureBoxStyle = field(default_factory=SignatureBoxStyle)
    
    # Style overrides per tag type
    style_overrides: Dict[str, SignatureBoxStyle] = field(default_factory=default_style_overrides)
    
    def get_style_for_tag(self, tag_type: str) -> SignatureBoxStyle:
        """Get the style for a specific tag type"""
        if tag_type in self.style_overrides:
            return self.style_overrides[tag_type]
        return self.default_style