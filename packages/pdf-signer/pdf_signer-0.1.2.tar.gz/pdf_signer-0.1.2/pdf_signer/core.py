# pdf_signer/core.py
import os
import re
from io import BytesIO
from typing import Dict, List, Tuple, Optional, Any, Pattern

import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfReader, PdfWriter

from .config import SignerConfig, SignatureBoxStyle
from .exceptions import PDFSignerError

class PDFSigner:
    """Main class for PDF signing functionality"""
    
    def __init__(self, config: Optional[SignerConfig] = None):
        """Initialize with optional configuration"""
        self.config = config or SignerConfig()
    
    def find_tags_in_pdf(self, pdf_path: str):
        """Find tags in PDF that match the configured pattern"""
        try:
            doc = fitz.open(pdf_path)
            tag_positions = []
            field_mapping = {}
            field_count = {}
            found_tags = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                page_width = page.rect.width
                page_height = page.rect.height
                words = page.get_text("words")
                
                for word_info in words:
                    word = word_info[4]
                    match = self.config.tag_pattern.match(word)
                    if match:
                        # Get the tag components based on the pattern
                        tag_components = match.groups()
                        field_id = word
                        
                        # Track unique tags
                        if field_id not in found_tags:
                            found_tags.append(field_id)
                        
                        # Count occurrences for each tag
                        if field_id not in field_count:
                            field_count[field_id] = 0
                        field_count[field_id] += 1
                        
                        unique_id = f"{field_id}_{field_count[field_id]}"
                        
                        # Calculate box position
                        x0, y0, _, y1 = word_info[0:4]
                        text_height = y1 - y0
                        
                        # Get appropriate style for this tag
                        tag_type = tag_components[0] if len(tag_components) > 0 else field_id
                        style = self.config.get_style_for_tag(tag_type)
                        
                        y_center = y0 + (text_height / 2)
                        box_y0 = y_center - (style.box_height / 2)
                        box_y1 = box_y0 + style.box_height
                        proposed_width = min(style.box_width * 2, page_width - x0 - 40)
                        
                        field_rect = (
                            x0,
                            box_y0,
                            x0 + proposed_width,
                            box_y1,
                        )
                        
                        tag_positions.append(
                            {
                                "page": page_num,
                                "rect": field_rect,
                                "field_id": field_id,
                                "unique_id": unique_id,
                                "word_info": word_info,
                                "page_height": page_height,
                                "tag_type": tag_type,
                            }
                        )
                        
                        field_mapping[unique_id] = {
                            "page": page_num,
                            "rect": field_rect,
                            "word_info": word_info,
                            "page_height": page_height,
                            "tag_type": tag_type,
                        }
            
            doc.close()
            return tag_positions, field_mapping, found_tags
            
        except Exception as e:
            raise PDFSignerError(f"Error finding tags in PDF: {str(e)}")
    
    def create_form_field(self, canvas_obj, x0, y0, width, height, signature_data, tag_type=None):
        """Create a signature form field with custom styling"""
        # Get appropriate style for this tag
        style = self.config.get_style_for_tag(tag_type) if tag_type else self.config.default_style
        
        max_width = min(width * 1.5, letter[0] - x0 - 40)
        
        # Set border style
        if style.border_style == "dotted":
            canvas_obj.setDash([2, 2])
        elif style.border_style == "dashed":
            canvas_obj.setDash([4, 2])
        else:  # solid
            canvas_obj.setDash([])
            
        # Set border color and width
        canvas_obj.setStrokeColorRGB(*style.border_color)
        canvas_obj.setLineWidth(style.border_width)
        
        # Set background color
        canvas_obj.setFillColorRGB(*style.background_color)
        
        # Draw the box
        canvas_obj.rect(x0, y0, max_width, height*1.3, fill=1, stroke=1)
        
        # Reset dash
        canvas_obj.setDash([])
        
        # Set text color
        canvas_obj.setFillColorRGB(*style.text_color)
        
        # Calculate font sizes
        name_font_size = min(height * style.name_font_size_factor, style.max_name_font_size)
        meta_font_size = min(height * style.meta_font_size_factor, style.max_meta_font_size)
        
        # Draw rows based on configuration
        row_data = style.row_data
        row_count = len(row_data)
        row_height = height / (row_count + 0.5)  # Add some padding
        
        for i, row_key in enumerate(row_data):
            y_pos = y0 + height - (i * row_height) - (row_height * 0.5)
            
            if row_key.lower() == "name":
                # Draw name with special formatting
                canvas_obj.setFont(style.name_font, name_font_size)
                username = signature_data.get("name", "")
                if len(username) > 17:
                    username = username[:13] + "..."
                canvas_obj.drawString(x0 + 3, y_pos, username)
            else:
                # Draw other fields
                canvas_obj.setFont(style.meta_font, meta_font_size)
                
                # Check if the row is a label or a value
                if row_key in signature_data:
                    # It's a direct value
                    text = f"{row_key}:{signature_data.get(row_key)}"
                else:
                    # It's a label, look for matching value
                    value_key = row_key.replace(":", "").strip()
                    if value_key in signature_data:
                        text = f"{row_key} {signature_data.get(value_key)}"
                    else:
                        text = row_key
                
                canvas_obj.drawString(x0 + 3, y_pos, text)
        
        # Draw tick image if provided
        if "tick_image_path" in signature_data and os.path.exists(signature_data["tick_image_path"]):
            tick_image = ImageReader(signature_data["tick_image_path"])
            tick_size = height * style.tick_image_size_factor
            
            # Calculate position based on configured factors
            tick_x = x0 + (max_width * style.tick_image_position[0])
            tick_y = y0 + (height * style.tick_image_position[1])
            
            canvas_obj.drawImage(
                tick_image,
                tick_x,
                tick_y,
                width=tick_size,
                height=tick_size,
                mask="auto",
            )
    
    def fill_signature_fields(self, input_pdf, output_pdf, signature_values):
        """Fill signature fields in the PDF"""
        try:
            tag_positions, _, found_tags = self.find_tags_in_pdf(input_pdf)
            reader = PdfReader(input_pdf)
            writer = PdfWriter()
            page_modifications = {}
            
            for pos in tag_positions:
                page_num = pos["page"]
                field_id = pos["field_id"]
                tag_type = pos.get("tag_type")
                
                if field_id in signature_values:
                    if page_num not in page_modifications:
                        page_modifications[page_num] = []
                    
                    # Transform coordinates from PDF to reportLab coordinate system
                    x0, y0, x1, y1 = pos["rect"]
                    page_height = pos["page_height"]
                    
                    # Convert to reportLab coordinates
                    rl_y0 = page_height - y1
                    
                    page_modifications[page_num].append(
                        {
                            "rect": (x0, rl_y0, x1 - x0, y1 - y0),
                            "signature_data": signature_values[field_id],
                            "tag_type": tag_type,
                        }
                    )
            
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                if page_num in page_modifications:
                    packet = BytesIO()
                    c = canvas.Canvas(packet, pagesize=letter)
                    
                    for mod in page_modifications[page_num]:
                        x0, y0, width, height = mod["rect"]
                        self.create_form_field(
                            c, x0, y0, width, height, 
                            mod["signature_data"], 
                            mod.get("tag_type")
                        )
                    
                    c.save()
                    packet.seek(0)
                    overlay = PdfReader(packet).pages[0]
                    page.merge_page(overlay)
                
                writer.add_page(page)
            
            with open(output_pdf, "wb") as output_file:
                writer.write(output_file)
            
            return True, len(tag_positions), found_tags
        
        except Exception as e:
            raise PDFSignerError(f"Error filling signature fields: {str(e)}")