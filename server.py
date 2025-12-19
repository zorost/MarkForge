#!/usr/bin/env python3
"""
MarkForge - Professional Document Converter
Enterprise-grade document conversion by Zorost Intelligence
"""

from flask import Flask, render_template, request, jsonify, Response
import markdown
from markitdown import MarkItDown
import tempfile
import os
from pathlib import Path

# xhtml2pdf for PDF generation (pure Python, works in bundled apps)
try:
    from xhtml2pdf import pisa
    import io
    HAS_XHTML2PDF = True
except ImportError:
    HAS_XHTML2PDF = False
    print("xhtml2pdf not available.")

# Playwright is optional - used for high-quality PDF generation (development only)
try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max upload

# Initialize MarkItDown converter
md_converter = MarkItDown()

# Professional PDF CSS - Compatible with xhtml2pdf (no external dependencies)
PDF_CSS = """
@page {
    size: A4;
    margin: 20mm 18mm;
}

* {
    box-sizing: border-box;
}

body {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.6;
    color: #1a1a1a;
    background: white;
    margin: 0;
    padding: 0;
}

/* Section wrapper for keeping headings with content */
section, article, .section {
    page-break-inside: avoid;
    break-inside: avoid;
}

/* Headings - NEVER break after heading, keep with next content */
h1, h2, h3, h4, h5, h6 {
    font-weight: 600;
    line-height: 1.3;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    color: #111;
    page-break-after: avoid !important;
    break-after: avoid !important;
    page-break-inside: avoid;
    break-inside: avoid;
}

h1 {
    font-size: 24pt;
    font-weight: 700;
    border-bottom: 3px solid #ff6b00;
    padding-bottom: 0.3em;
    margin-top: 0;
    margin-bottom: 1em;
}

h2 {
    font-size: 18pt;
    color: #ff6b00;
    margin-top: 1.8em;
    page-break-before: auto;
}

h3 {
    font-size: 14pt;
    color: #333;
}

h4 {
    font-size: 12pt;
    color: #444;
}

h5, h6 {
    font-size: 10pt;
    color: #555;
}

/* First element after heading - never break before */
h1 + *, h2 + *, h3 + *, h4 + *, h5 + *, h6 + * {
    page-break-before: avoid !important;
    break-before: avoid !important;
}

/* Paragraphs */
p {
    margin: 0 0 1em 0;
    orphans: 4;
    widows: 4;
}

strong, b {
    font-weight: 600;
}

em, i {
    font-style: italic;
}

a {
    color: #ff6b00;
    text-decoration: none;
}

/* Code blocks - Proper monospace for ASCII diagrams */
code {
    font-family: Courier, monospace;
    font-size: 0.85em;
    background: #f4f4f5;
    padding: 0.15em 0.4em;
    border-radius: 3px;
    color: #c2410c;
}

pre {
    font-family: Courier, monospace;
    font-size: 8pt;
    line-height: 1.4;
    background: #fafafa;
    border: 1px solid #e4e4e7;
    border-left: 4px solid #ff6b00;
    color: #1a1a1a;
    padding: 1em 1.2em;
    margin: 1em 0;
    overflow-x: visible;
    white-space: pre;
    page-break-inside: avoid;
    break-inside: avoid;
}

pre code {
    background: none;
    padding: 0;
    border-radius: 0;
    color: inherit;
    font-size: inherit;
    white-space: pre;
}

/* Blockquotes - keep together */
blockquote {
    margin: 1em 0;
    padding: 0.8em 1.2em;
    border-left: 4px solid #ff6b00;
    background: #fff7ed;
    color: #444;
    font-style: italic;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}

blockquote p {
    margin: 0;
}

blockquote p + p {
    margin-top: 0.5em;
}

/* Tables - NEVER break inside */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 9pt;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}

thead {
    display: table-header-group;
}

tbody {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}

tr {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}

th {
    background: #374151;
    color: white;
    font-weight: 600;
    text-align: left;
    padding: 0.6em 0.8em;
    border: 1px solid #4b5563;
    font-size: 8pt;
}

td {
    border: 1px solid #e4e4e7;
    padding: 0.5em 0.8em;
    background: white;
    vertical-align: top;
}

tr:nth-child(even) td {
    background: #fafafa;
}

/* Lists - avoid breaking list items */
ul, ol {
    margin: 1em 0;
    padding-left: 1.8em;
}

li {
    margin: 0.3em 0;
    line-height: 1.5;
    page-break-inside: avoid;
    break-inside: avoid;
}

li > p {
    margin: 0;
}

li ul, li ol {
    margin: 0.3em 0;
}

/* Horizontal rule */
hr {
    border: none;
    border-top: 2px solid #e4e4e7;
    margin: 2em 0;
    page-break-after: avoid;
}

/* Images */
img {
    max-width: 100%;
    height: auto;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}

/* Code highlighting */
.codehilite {
    background: #fafafa;
    border: 1px solid #e4e4e7;
    border-left: 4px solid #ff6b00;
    padding: 1em 1.2em;
    margin: 1em 0;
    overflow-x: visible;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}

.codehilite pre {
    margin: 0;
    padding: 0;
    background: none;
    border: none;
    border-left: none;
}

/* Container divs that should stay together */
div {
    page-break-inside: avoid;
    break-inside: avoid;
}

/* Orphans and widows */
p, li, blockquote, td {
    orphans: 4;
    widows: 4;
}
"""


def convert_markdown_to_html(markdown_text: str) -> str:
    """Convert Markdown to HTML with full extension support."""
    md = markdown.Markdown(
        extensions=[
            'tables',
            'fenced_code',
            'codehilite',
            'toc',
            'nl2br',
            'sane_lists',
        ],
        extension_configs={
            'codehilite': {
                'css_class': 'codehilite',
                'linenums': False,
                'guess_lang': True,
            }
        }
    )
    return md.convert(markdown_text)


def generate_pdf_bytes(markdown_text: str, page_size: str = "A4") -> bytes:
    """Generate PDF from Markdown using xhtml2pdf or Playwright."""
    html_content = convert_markdown_to_html(markdown_text)
    
    # Build complete HTML document with xhtml2pdf-compatible CSS
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>{PDF_CSS}</style>
</head>
<body>
{html_content}
</body>
</html>"""
    
    # Try xhtml2pdf first (pure Python, works in bundled apps)
    if HAS_XHTML2PDF:
        try:
            result = io.BytesIO()
            pisa_status = pisa.CreatePDF(
                src=full_html,
                dest=result,
                encoding='UTF-8'
            )
            if pisa_status.err:
                raise Exception(f"xhtml2pdf error: {pisa_status.err}")
            return result.getvalue()
        except Exception as e:
            print(f"xhtml2pdf error: {e}")
            # Fall through to Playwright if xhtml2pdf fails
    
    # Try Playwright as fallback (for development with browser rendering)
    if HAS_PLAYWRIGHT:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            
            page.set_content(full_html, wait_until='networkidle')
            
            pdf_bytes = page.pdf(
                format=page_size if page_size in ['A4', 'A3', 'A5', 'Letter', 'Legal'] else 'A4',
                margin={
                    'top': '20mm',
                    'right': '18mm',
                    'bottom': '20mm',
                    'left': '18mm'
                },
                print_background=True,
                prefer_css_page_size=True
            )
            
            browser.close()
        
        return pdf_bytes
    
    raise Exception("No PDF generation library available. Please install xhtml2pdf.")


@app.route('/')
def index():
    """Serve the main application page."""
    return render_template('index.html')


@app.route('/api/preview', methods=['POST'])
def preview():
    """Generate HTML preview of Markdown."""
    try:
        data = request.get_json()
        markdown_text = data.get('markdown', '')
        
        if not markdown_text.strip():
            return jsonify({'html': '', 'success': True})
        
        html_content = convert_markdown_to_html(markdown_text)
        return jsonify({'html': html_content, 'success': True})
    
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/convert', methods=['POST'])
def convert():
    """Convert Markdown to PDF and return the file (JSON API)."""
    try:
        data = request.get_json()
        markdown_text = data.get('markdown', '')
        page_size = data.get('pageSize', 'A4')
        filename = data.get('filename', 'document.pdf')
        
        if not markdown_text.strip():
            return jsonify({'error': 'No content provided'}), 400
        
        # Generate PDF
        pdf_bytes = generate_pdf_bytes(markdown_text, page_size)
        
        # Return as downloadable file
        return Response(
            pdf_bytes,
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Content-Length': len(pdf_bytes)
            }
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download-pdf', methods=['POST'])
def download_pdf():
    """Convert Markdown to PDF via form submission (works better in desktop apps)."""
    try:
        markdown_text = request.form.get('markdown', '')
        page_size = request.form.get('pageSize', 'A4')
        
        if not markdown_text.strip():
            return "No content provided", 400
        
        # Generate PDF
        pdf_bytes = generate_pdf_bytes(markdown_text, page_size)
        
        # Return as downloadable file
        return Response(
            pdf_bytes,
            mimetype='application/pdf',
            headers={
                'Content-Disposition': 'attachment; filename="document.pdf"',
                'Content-Length': len(pdf_bytes)
            }
        )
    
    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route('/api/download-markdown', methods=['POST'])
def download_markdown():
    """Download markdown content as a file."""
    try:
        markdown_text = request.form.get('markdown', '')
        
        if not markdown_text.strip():
            return "No content provided", 400
        
        return Response(
            markdown_text.encode('utf-8'),
            mimetype='text/markdown',
            headers={
                'Content-Disposition': 'attachment; filename="document.md"',
            }
        )
    
    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route('/api/download-text', methods=['POST'])
def download_text():
    """Download plain text content as a file."""
    try:
        text = request.form.get('text', '')
        
        if not text.strip():
            return "No content provided", 400
        
        return Response(
            text.encode('utf-8'),
            mimetype='text/plain',
            headers={
                'Content-Disposition': 'attachment; filename="document.txt"',
            }
        )
    
    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route('/api/upload', methods=['POST'])
def upload():
    """Handle file upload and return markdown content."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read file content
        content = file.read().decode('utf-8')
        return jsonify({'content': content, 'success': True})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/doc-to-markdown', methods=['POST'])
def doc_to_markdown():
    """Convert PDF, Word, Excel, PowerPoint to Markdown using MarkItDown."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided', 'success': False}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected', 'success': False}), 400
        
        # Get file extension
        filename = file.filename.lower()
        
        # Save to temp file for processing
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name
        
        try:
            # Convert using MarkItDown
            result = md_converter.convert(tmp_path)
            markdown_content = result.text_content
            
            return jsonify({
                'markdown': markdown_content,
                'success': True
            })
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7861))
    app.run(host='0.0.0.0', port=port, debug=True)
