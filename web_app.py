#!/usr/bin/env python3
"""
MarkForge - Professional Markdown to PDF Converter
Enterprise-grade document conversion by Zorost Intelligence
"""

import gradio as gr
import markdown
from xhtml2pdf import pisa
import tempfile
import io
import os
from pathlib import Path

# Professional PDF CSS
PDF_CSS = """
@page {
    size: a4 portrait;
    margin: 2cm 2.5cm;
}

body {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1a1a1a;
}

h1 {
    font-size: 26pt;
    font-weight: bold;
    color: #0f172a;
    margin-top: 0;
    margin-bottom: 18pt;
    padding-bottom: 10pt;
    border-bottom: 2pt solid #2563eb;
}

h2 {
    font-size: 18pt;
    font-weight: bold;
    color: #1e293b;
    margin-top: 28pt;
    margin-bottom: 12pt;
}

h3 {
    font-size: 14pt;
    font-weight: bold;
    color: #334155;
    margin-top: 22pt;
    margin-bottom: 10pt;
}

h4 {
    font-size: 12pt;
    font-weight: bold;
    color: #475569;
    margin-top: 18pt;
    margin-bottom: 8pt;
}

p {
    margin-bottom: 12pt;
    text-align: justify;
}

a {
    color: #2563eb;
    text-decoration: none;
}

code {
    font-family: Courier, monospace;
    font-size: 9pt;
    background-color: #f1f5f9;
    padding: 2pt 4pt;
}

pre {
    font-family: Courier, monospace;
    font-size: 9pt;
    background-color: #1e293b;
    color: #e2e8f0;
    padding: 14pt;
    margin: 14pt 0;
    white-space: pre-wrap;
    word-wrap: break-word;
}

blockquote {
    border-left: 3pt solid #2563eb;
    padding-left: 16pt;
    margin: 16pt 0;
    margin-left: 0;
    color: #475569;
    font-style: italic;
    background-color: #f8fafc;
    padding: 12pt 16pt;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 16pt 0;
    font-size: 10pt;
}

th {
    background-color: #1e293b;
    color: white;
    font-weight: bold;
    text-align: left;
    padding: 10pt 12pt;
    border: 1pt solid #334155;
}

td {
    border: 1pt solid #e2e8f0;
    padding: 10pt 12pt;
}

tr:nth-child(even) td {
    background-color: #f8fafc;
}

ul, ol {
    margin-bottom: 12pt;
    padding-left: 24pt;
}

li {
    margin-bottom: 4pt;
}

hr {
    border: none;
    border-top: 1pt solid #e2e8f0;
    margin: 24pt 0;
}

.header-text {
    font-size: 9pt;
    color: #64748b;
    text-align: center;
    margin-bottom: 20pt;
}

.footer-text {
    font-size: 9pt;
    color: #64748b;
    text-align: center;
    margin-top: 20pt;
    padding-top: 12pt;
    border-top: 1pt solid #e2e8f0;
}

.page-break {
    page-break-before: always;
}
"""

# Custom theme CSS for Gradio
CUSTOM_CSS = """
.gradio-container {
    max-width: 1400px !important;
    margin: auto !important;
}

.app-header {
    text-align: center;
    padding: 48px 24px 36px;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    border-radius: 20px;
    margin-bottom: 28px;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.15);
}

.app-title {
    font-size: 48px;
    font-weight: 800;
    color: white;
    margin: 0;
    letter-spacing: -2px;
}

.brand-accent {
    background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.app-tagline {
    font-size: 16px;
    color: #94a3b8;
    margin-top: 12px;
}

.zorost-link {
    color: #60a5fa !important;
    text-decoration: none !important;
    font-weight: 500;
}

.zorost-link:hover {
    color: #93c5fd !important;
}

.section-title {
    font-size: 15px;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.section-title::before {
    content: '';
    width: 4px;
    height: 18px;
    background: #2563eb;
    border-radius: 2px;
}

.footer {
    text-align: center;
    padding: 28px 20px;
    color: #64748b;
    font-size: 14px;
    border-top: 1px solid #e2e8f0;
    margin-top: 36px;
    background: #f8fafc;
    border-radius: 0 0 16px 16px;
}

.footer-brand {
    font-weight: 700;
    color: #1e293b;
}

.footer-link {
    color: #2563eb !important;
    text-decoration: none !important;
    font-weight: 500;
}

.footer-link:hover {
    text-decoration: underline !important;
}

.preview-container {
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    background: white;
    min-height: 450px;
    overflow: auto;
}

.options-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
}

.status-success {
    color: #059669 !important;
    font-weight: 600;
}

.status-error {
    color: #dc2626 !important;
    font-weight: 600;
}

.generate-btn {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
    border: none !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    padding: 14px 36px !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
    transition: all 0.2s ease !important;
}

.generate-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.45) !important;
}
"""


def convert_md_to_html(markdown_text: str) -> str:
    """Convert Markdown to HTML."""
    md = markdown.Markdown(
        extensions=[
            'tables',
            'fenced_code',
            'codehilite',
            'toc',
            'nl2br',
            'sane_lists',
        ]
    )
    return md.convert(markdown_text)


def generate_pdf(markdown_text: str, page_size: str = "A4", 
                 header_text: str = "", footer_text: str = "") -> str:
    """Generate PDF from Markdown content."""
    if not markdown_text.strip():
        return None
    
    # Convert Markdown to HTML
    html_content = convert_md_to_html(markdown_text)
    
    # Build header/footer sections
    header_html = f'<div class="header-text">{header_text}</div>' if header_text else ""
    footer_html = f'<div class="footer-text">{footer_text}</div>' if footer_text else ""
    
    # Page size mapping
    page_sizes = {
        "A4": "a4 portrait",
        "Letter": "letter portrait",
        "Legal": "legal portrait",
        "A3": "a3 portrait",
        "A5": "a5 portrait",
    }
    
    page_css = PDF_CSS.replace("size: a4 portrait;", f"size: {page_sizes.get(page_size, 'a4 portrait')};")
    
    # Build full HTML document
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>{page_css}</style>
    </head>
    <body>
        {header_html}
        {html_content}
        {footer_html}
    </body>
    </html>
    """
    
    # Generate PDF
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        output_path = f.name
    
    with open(output_path, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(full_html, dest=pdf_file)
    
    if pisa_status.err:
        return None
    
    return output_path


def preview_html(markdown_text: str) -> str:
    """Generate HTML preview of Markdown."""
    if not markdown_text.strip():
        return """
        <div style="display: flex; align-items: center; justify-content: center; 
                    height: 400px; color: #94a3b8; font-size: 15px;">
            Enter Markdown content to see live preview
        </div>
        """
    
    html_content = convert_md_to_html(markdown_text)
    
    # Wrap in styled container
    preview = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                font-size: 14px; line-height: 1.7; color: #1e293b; padding: 24px;">
        <style>
            .preview h1 {{ font-size: 26px; font-weight: 700; color: #0f172a; 
                          border-bottom: 3px solid #2563eb; padding-bottom: 10px; margin-bottom: 20px; }}
            .preview h2 {{ font-size: 20px; font-weight: 600; color: #1e293b; margin-top: 28px; margin-bottom: 14px; }}
            .preview h3 {{ font-size: 16px; font-weight: 600; color: #334155; margin-top: 22px; }}
            .preview code {{ background: #f1f5f9; padding: 3px 7px; border-radius: 5px; 
                            font-size: 13px; color: #be185d; font-family: 'SF Mono', Monaco, monospace; }}
            .preview pre {{ background: #0f172a; color: #e2e8f0; padding: 18px; border-radius: 10px; 
                           overflow-x: auto; font-size: 13px; line-height: 1.5; }}
            .preview pre code {{ background: none; color: inherit; padding: 0; }}
            .preview blockquote {{ border-left: 4px solid #2563eb; padding: 14px 18px; margin: 18px 0; 
                                  margin-left: 0; color: #475569; font-style: italic; 
                                  background: #f8fafc; border-radius: 0 8px 8px 0; }}
            .preview table {{ width: 100%; border-collapse: collapse; margin: 18px 0; }}
            .preview th {{ background: #1e293b; color: white; padding: 12px 14px; text-align: left; font-weight: 600; }}
            .preview td {{ border: 1px solid #e2e8f0; padding: 12px 14px; }}
            .preview tr:nth-child(even) td {{ background: #f8fafc; }}
            .preview a {{ color: #2563eb; text-decoration: none; }}
            .preview a:hover {{ text-decoration: underline; }}
            .preview hr {{ border: none; border-top: 2px solid #e2e8f0; margin: 28px 0; }}
            .preview ul, .preview ol {{ padding-left: 24px; }}
            .preview li {{ margin-bottom: 6px; }}
        </style>
        <div class="preview">
            {html_content}
        </div>
    </div>
    """
    return preview


def load_markdown_file(file) -> str:
    """Load Markdown from uploaded file."""
    if file is None:
        return ""
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error loading file: {str(e)}"


# Sample Markdown
SAMPLE_MARKDOWN = """# Welcome to MarkForge

**MarkForge** is a professional Markdown to PDF converter developed by **Zorost Intelligence**.

## Key Features

- Professional PDF output with enterprise styling
- Live preview as you type
- Multiple page size options (A4, Letter, Legal, A3, A5)
- Custom headers and footers
- Full Markdown support including tables and code blocks

## Code Example

Here's a Python code sample:

```python
def convert_document(markdown_text):
    \"\"\"Convert Markdown to beautifully formatted PDF.\"\"\"
    html = markdown_to_html(markdown_text)
    pdf = generate_pdf(html)
    return pdf
```

## Table Example

| Feature | Description | Status |
|---------|-------------|--------|
| Markdown Parsing | Full GFM support | Complete |
| PDF Generation | Professional styling | Complete |
| Code Highlighting | Syntax highlighting | Complete |
| Table Support | Full table rendering | Complete |

## Blockquote

> "DocForge transforms how we create professional documents. It's fast, reliable, and produces beautiful results."
> 
> — Enterprise Customer

---

### Getting Started

1. Enter or paste your Markdown content
2. Preview in real-time on the right
3. Configure PDF options (page size, headers, footers)
4. Click **Generate PDF** to download

---

*Powered by Zorost Intelligence*
"""


def create_app():
    """Create the Gradio application."""
    
    with gr.Blocks(title="MarkForge - Markdown to PDF") as app:
        
        # Header
        gr.HTML("""
        <div class="app-header">
            <h1 class="app-title">Mark<span class="brand-accent">Forge</span></h1>
            <p style="color: #64748b; font-size: 13px; margin-top: 6px;">
                by <a href="https://zorost.com" target="_blank" class="zorost-link">Zorost Intelligence</a>
            </p>
            <p class="app-tagline">
                Professional Markdown to PDF Converter
            </p>
        </div>
        """)
        
        with gr.Row(equal_height=True):
            # Left Column - Editor
            with gr.Column(scale=1):
                gr.HTML('<div class="section-title">Markdown Editor</div>')
                
                file_upload = gr.File(
                    label="Upload .md file",
                    file_types=[".md", ".markdown", ".txt"],
                    type="filepath"
                )
                
                md_input = gr.Textbox(
                    label="",
                    placeholder="Enter your Markdown here...",
                    lines=22,
                    max_lines=50,
                    value=SAMPLE_MARKDOWN,
                    show_label=False
                )
                
                with gr.Row():
                    sample_btn = gr.Button("Load Sample", size="sm", variant="secondary")
                    clear_btn = gr.Button("Clear", size="sm", variant="secondary")
            
            # Right Column - Preview
            with gr.Column(scale=1):
                gr.HTML('<div class="section-title">Live Preview</div>')
                preview_output = gr.HTML(
                    value=preview_html(SAMPLE_MARKDOWN),
                    elem_classes=["preview-container"]
                )
        
        # Options Section
        gr.HTML('<div class="section-title" style="margin-top: 24px;">PDF Options</div>')
        
        with gr.Row():
            with gr.Column(scale=1):
                page_size = gr.Dropdown(
                    choices=["A4", "Letter", "Legal", "A3", "A5"],
                    value="A4",
                    label="Page Size"
                )
            with gr.Column(scale=1):
                header_text = gr.Textbox(
                    label="Header Text",
                    placeholder="Optional header text",
                    max_lines=1
                )
            with gr.Column(scale=1):
                footer_text = gr.Textbox(
                    label="Footer Text",
                    placeholder="Optional footer text",
                    max_lines=1
                )
        
        # Generate Button
        with gr.Row():
            with gr.Column():
                convert_btn = gr.Button(
                    "Generate PDF",
                    variant="primary",
                    size="lg",
                    elem_classes=["generate-btn"]
                )
        
        # Output
        with gr.Row():
            with gr.Column(scale=2):
                pdf_output = gr.File(label="Download PDF", interactive=False)
            with gr.Column(scale=1):
                status_output = gr.Markdown("")
        
        # Footer
        gr.HTML("""
        <div class="footer">
            <p>
                <span class="footer-brand">MarkForge</span> by 
                <a href="https://zorost.com" target="_blank" class="footer-link">Zorost Intelligence</a>
            </p>
            <p style="margin-top: 8px; color: #94a3b8; font-size: 13px;">
                Enterprise-grade document conversion platform
            </p>
        </div>
        """)
        
        # Event handlers
        def update_preview(md_text):
            return preview_html(md_text)
        
        def load_file(file):
            if file:
                content = load_markdown_file(file)
                return content, preview_html(content)
            return "", preview_html("")
        
        def convert_to_pdf(md_text, page, header, footer):
            if not md_text.strip():
                return None, '<p class="status-error">Please enter Markdown content</p>'
            try:
                pdf_path = generate_pdf(md_text, page, header, footer)
                if pdf_path:
                    return pdf_path, '<p class="status-success">PDF generated successfully</p>'
                else:
                    return None, '<p class="status-error">PDF generation failed</p>'
            except Exception as e:
                return None, f'<p class="status-error">Error: {str(e)}</p>'
        
        def clear_all():
            return "", preview_html(""), None, ""
        
        def load_sample():
            return SAMPLE_MARKDOWN, preview_html(SAMPLE_MARKDOWN)
        
        # Wire up events
        md_input.change(update_preview, inputs=[md_input], outputs=[preview_output])
        file_upload.change(load_file, inputs=[file_upload], outputs=[md_input, preview_output])
        convert_btn.click(
            convert_to_pdf,
            inputs=[md_input, page_size, header_text, footer_text],
            outputs=[pdf_output, status_output]
        )
        clear_btn.click(clear_all, outputs=[md_input, preview_output, pdf_output, status_output])
        sample_btn.click(load_sample, outputs=[md_input, preview_output])
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False,
        show_error=True,
        css=CUSTOM_CSS,
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="slate",
            neutral_hue="slate",
        )
    )
