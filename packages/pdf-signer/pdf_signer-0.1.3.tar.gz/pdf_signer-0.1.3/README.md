# PDF Signer

A customizable Python package for adding signature boxes to PDF documents based on text tags.

## Features

- Add signature boxes to PDFs at positions marked by customizable tags
- Highly configurable appearance of signature boxes (colors, sizes, borders)
- Customizable text content and layout in signature boxes
- Support for verification images/badges
- Flexible tag pattern matching

## Installation

```bash
pip install pdf-signer
```

## Basic Usage

```python
from pdf_signer import PDFSigner

# Create a signer with default settings
signer = PDFSigner()

# Define signature data
signature_values = {
    "int_p1": {
        "name": "John Doe",
        "Date": "14.03.25 at 10:30:45 AM",
        "tick_image_path": "path/to/bluetick.png",
        "IP": "192.168.1.1",
    }
}

# Process the PDF
success, count, found_tags = signer.fill_signature_fields(
    "input.pdf", "output.pdf", signature_values
)

print(f"Found tags: {found_tags}")
print(f"Processed {count} signature fields")
```

## Advanced Configuration

You can customize almost every aspect of the signature boxes:

```python
from pdf_signer import PDFSigner, SignerConfig, SignatureBoxStyle

# Create custom style
custom_style = SignatureBoxStyle(
    box_width=40,
    box_height=35,
    background_color=(0.9, 0.9, 1.0),  # Light purple
    border_color=(0.5, 0.0, 0.5),  # Purple
    border_style="dashed",
    row_data=["name", "Signed:", "Date", "IP: ", "IP"]
)

# Create configuration with custom tag pattern
config = SignerConfig(
    tag_pattern_str=r"signature_([a-z]+)",  # Custom tag pattern
    default_style=custom_style
)

# Create signer with custom config
signer = PDFSigner(config)
```

## Customizing Tags

By default, the package looks for tags like `int_p1` or `count_p1`, but you can define any pattern:

```python
config = SignerConfig(
    tag_pattern_str=r"(?P<type>sign|approve|review)_(?P<id>\d+)"
)
```

## Different Styles for Different Tags

You can define different styles for different types of signature boxes:

```python
config = SignerConfig(
    tag_pattern_str=r"(ceo|manager|staff)_(\d+)",
    style_overrides={
        "ceo": SignatureBoxStyle(
            background_color=(1.0, 0.9, 0.9),  # Light red
            row_data=["name", "CEO Approval", "Date"]
        ),
        "manager": SignatureBoxStyle(
            background_color=(0.9, 1.0, 0.9),  # Light green
            row_data=["name", "Manager Approval", "Date"]
        )
    }
)
```

## License

MIT