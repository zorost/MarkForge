# MarkForge

**Professional Document Converter**

MarkForge is an enterprise-grade document conversion platform that transforms various file formats to Markdown and generates professional PDF documents. Built on top of [Microsoft MarkItDown](https://github.com/microsoft/markitdown), MarkForge provides both a desktop application and a web-based interface for seamless document processing.

---

## Overview

MarkForge bridges the gap between proprietary document formats and universal Markdown. Whether you need to extract content from PDFs, convert Word documents for technical documentation, or generate beautifully styled PDF reports from Markdown, MarkForge handles it all with precision and speed.

---

## Key Features

### Document to Markdown Conversion

Convert a wide range of file formats to clean, structured Markdown:

| Format | Extensions | Description |
|--------|------------|-------------|
| PDF Documents | .pdf | Extract text and structure from PDF files |
| Microsoft Word | .docx, .doc | Full support for Word documents with formatting |
| Microsoft Excel | .xlsx, .xls | Convert spreadsheets to Markdown tables |
| Microsoft PowerPoint | .pptx, .ppt | Extract slide content and speaker notes |
| HTML | .html, .htm | Convert web pages to Markdown |
| Images | .jpg, .png, .gif, .webp | OCR-powered text extraction |
| EPUB | .epub | Extract content from e-books |
| Data Files | .csv, .json, .xml | Convert structured data to Markdown tables |
| Archives | .zip | Process contents of compressed archives |

### Markdown to PDF Generation

Transform Markdown content into professionally styled PDF documents with:

- Multiple page size options (A4, Letter, Legal, A3, A5)
- Custom headers and footers
- Syntax-highlighted code blocks
- Professional table styling
- Smart page break handling
- High-quality typography

### Dual Interface Options

**Desktop Application**
- Native macOS application with drag-and-drop support
- Offline capability for secure document processing
- Light and dark theme support
- Real-time conversion feedback

**Web Application**
- Browser-based interface accessible from any device
- Live preview as you type
- No installation required
- Deployable on your own infrastructure

---

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Quick Start

1. Clone the repository:

```bash
git clone https://github.com/zorost/MarkForge.git
cd MarkForge
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. For web application, install Playwright browsers:

```bash
playwright install chromium
```

### Running the Web Application

```bash
python server.py
```

The application will be available at `http://localhost:7861`

### Running the Desktop Application

```bash
python app.py
```

---

## Usage

### Web Interface

1. Select the conversion mode from the dropdown menu
2. Upload your document or paste Markdown content
3. Preview the output in real-time
4. Download the converted file

### Desktop Application

1. Launch the application
2. Drag and drop a file onto the window, or click to browse
3. View the converted Markdown in the output panel
4. Save as Markdown (.md) or export to PDF

### Supported Conversions

**To Markdown:**
- PDF to Markdown
- Word to Markdown
- PowerPoint to Markdown
- Excel to Markdown
- HTML to Markdown
- Image to Markdown (with OCR)
- EPUB to Markdown
- CSV/JSON/XML to Markdown
- ZIP to Markdown

**From Markdown:**
- Markdown to PDF
- Markdown to Plain Text

---

## Configuration

### PDF Styling

The PDF output is styled with professional typography and layout:

- Clean, readable fonts (Inter, JetBrains Mono)
- Proper heading hierarchy with accent colors
- Code blocks with syntax highlighting
- Tables with alternating row colors
- Smart page break handling to prevent orphaned headings

### Page Sizes

| Size | Dimensions |
|------|------------|
| A4 | 210mm x 297mm |
| Letter | 8.5in x 11in |
| Legal | 8.5in x 14in |
| A3 | 297mm x 420mm |
| A5 | 148mm x 210mm |

---

## API Reference

The web application provides a REST API for programmatic access:

### Preview Markdown

```
POST /api/preview
Content-Type: application/json

{
    "markdown": "# Your Markdown Content"
}
```

### Convert to PDF

```
POST /api/convert
Content-Type: application/json

{
    "markdown": "# Your Markdown Content",
    "pageSize": "A4",
    "filename": "document.pdf"
}
```

### Convert Document to Markdown

```
POST /api/doc-to-markdown
Content-Type: multipart/form-data

file: [Your document file]
```

---

## Deployment

### Railway Deployment

MarkForge includes configuration for Railway deployment:

```bash
# railway.json and Procfile are included
railway up
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install chromium --with-deps

COPY . .
EXPOSE 7861
CMD ["python", "server.py"]
```

---

## Building Desktop Applications

### macOS Build

On macOS, run the build script:

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install pywebview pyinstaller

# Build the app
python build_mac.py

# Or use PyInstaller directly
pyinstaller --clean MarkForge.spec
```

The app will be created at `dist/MarkForge.app` and automatically copied to `/Applications/`.

### Windows Build

On Windows, run:

```powershell
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install pywebview pyinstaller pythonnet

# Build the app
python build_windows.py

# Or use PyInstaller directly
pyinstaller --clean MarkForge-Windows.spec
```

The executable will be created at `dist\MarkForge\MarkForge.exe`.

### Build Requirements

| Platform | Requirements |
|----------|-------------|
| macOS | Python 3.10+, Xcode Command Line Tools |
| Windows | Python 3.10+, .NET Framework 4.6.2+ |

---

## Technology Stack

- **Core Engine:** Microsoft MarkItDown
- **PDF Generation:** Playwright (Chromium-based rendering)
- **Web Framework:** Flask
- **Desktop GUI:** CustomTkinter
- **Markdown Processing:** Python-Markdown

---

## About Zorost Intelligence

**MarkForge is developed and maintained by Zorost Intelligence.**

Zorost Intelligence specializes in building intelligent automation solutions for businesses. We focus on creating tools that enhance productivity, streamline workflows, and leverage AI capabilities to solve complex business challenges.

### What We Offer

**Document Automation**
Transform how your organization handles documents. From conversion and extraction to intelligent processing, we build solutions that reduce manual work and improve accuracy.

**Custom AI Solutions**
Leverage the power of artificial intelligence tailored to your specific business needs. We develop custom AI applications that integrate seamlessly with your existing workflows.

**Enterprise Integration**
Connect disparate systems and automate data flow across your organization. Our integration solutions ensure your tools work together efficiently.

**Consulting Services**
Strategic guidance on implementing AI and automation in your business. We help identify opportunities and develop roadmaps for digital transformation.

### Get in Touch

We welcome collaboration and inquiries from businesses looking to modernize their document workflows or explore AI-powered solutions.

- Website: [https://zorost.com](https://zorost.com)
- GitHub: [https://github.com/zorost](https://github.com/zorost)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

MarkForge is free to use, modify, and distribute. We encourage contributions from the community and welcome feature requests and bug reports.

---

## Acknowledgments

- [Microsoft MarkItDown](https://github.com/microsoft/markitdown) - The core conversion engine
- [Playwright](https://playwright.dev/) - Browser automation for PDF generation
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern GUI framework

---

## Contributing

Contributions are welcome. Please feel free to submit pull requests or open issues for bugs and feature requests.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

Developed with precision by **Zorost Intelligence**
