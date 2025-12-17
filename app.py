#!/usr/bin/env python3
"""
MarkItDown Desktop App
A professional GUI for Microsoft's MarkItDown library.
Converts various file formats to Markdown, with PDF export.
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import threading
import os
import sys
from pathlib import Path

# Import MarkItDown
try:
    from markitdown import MarkItDown
except ImportError:
    print("Please install markitdown: pip install 'markitdown[all]'")
    sys.exit(1)

# Import PDF export libraries
try:
    import markdown
    from weasyprint import HTML, CSS
    HAS_PDF_EXPORT = True
except ImportError:
    HAS_PDF_EXPORT = False
    print("PDF export not available. Install: pip install markdown weasyprint")


# Color palette - Enterprise grade
COLORS = {
    "primary": "#2563eb",
    "primary_hover": "#1d4ed8",
    "secondary": "#0f172a",
    "accent": "#3b82f6",
    "success": "#059669",
    "error": "#dc2626",
    "warning": "#d97706",
    "surface_dark": "#0f172a",
    "surface_dark_alt": "#1e293b",
    "surface_light": "#f8fafc",
    "surface_light_alt": "#e2e8f0",
    "text_primary_dark": "#f1f5f9",
    "text_secondary_dark": "#94a3b8",
    "text_primary_light": "#0f172a",
    "text_secondary_light": "#64748b",
    "border_dark": "#334155",
    "border_light": "#cbd5e1",
}

# PDF styling
PDF_CSS = """
@page {
    size: A4;
    margin: 2.5cm;
}
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1a1a1a;
}
h1 { font-size: 24pt; font-weight: 700; margin-top: 0; margin-bottom: 16pt; color: #0f172a; }
h2 { font-size: 18pt; font-weight: 600; margin-top: 24pt; margin-bottom: 12pt; color: #1e293b; }
h3 { font-size: 14pt; font-weight: 600; margin-top: 20pt; margin-bottom: 10pt; color: #334155; }
h4 { font-size: 12pt; font-weight: 600; margin-top: 16pt; margin-bottom: 8pt; }
p { margin-bottom: 12pt; }
code {
    font-family: 'SF Mono', Monaco, 'Courier New', monospace;
    font-size: 9pt;
    background-color: #f1f5f9;
    padding: 2pt 4pt;
    border-radius: 3pt;
}
pre {
    font-family: 'SF Mono', Monaco, 'Courier New', monospace;
    font-size: 9pt;
    background-color: #f1f5f9;
    padding: 12pt;
    border-radius: 6pt;
    overflow-x: auto;
    white-space: pre-wrap;
}
blockquote {
    border-left: 3pt solid #3b82f6;
    padding-left: 16pt;
    margin-left: 0;
    color: #475569;
    font-style: italic;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin: 16pt 0;
}
th, td {
    border: 1pt solid #e2e8f0;
    padding: 8pt 12pt;
    text-align: left;
}
th {
    background-color: #f8fafc;
    font-weight: 600;
}
ul, ol { margin-bottom: 12pt; padding-left: 24pt; }
li { margin-bottom: 4pt; }
a { color: #2563eb; text-decoration: none; }
hr { border: none; border-top: 1pt solid #e2e8f0; margin: 24pt 0; }
img { max-width: 100%; height: auto; }
"""


class MarkItDownApp(ctk.CTk, TkinterDnD.DnDWrapper):
    """Main application window for MarkItDown converter."""
    
    TK_SILENCE_DEPRECATION = 1
    
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        
        # Configure window
        self.title("MarkItDown")
        self.geometry("960x750")
        self.minsize(850, 700)
        
        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Initialize MarkItDown
        self.md = MarkItDown(enable_plugins=False)
        self.current_file = None
        self.converted_content = None
        
        # Build UI
        self._create_header()
        self._create_drop_zone()
        self._create_output_area()
        self._create_footer()
        
    def _create_header(self):
        """Create the header with title and description."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=48, pady=(36, 24))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # App title
        title_label = ctk.CTkLabel(
            header_frame,
            text="MarkItDown",
            font=ctk.CTkFont(family="SF Pro Display", size=38, weight="bold"),
            text_color=(COLORS["text_primary_light"], COLORS["text_primary_dark"])
        )
        title_label.grid(row=0, column=0, sticky="w")
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Convert files to Markdown and PDF",
            font=ctk.CTkFont(family="SF Pro Text", size=16),
            text_color=(COLORS["text_secondary_light"], COLORS["text_secondary_dark"])
        )
        subtitle_label.grid(row=1, column=0, sticky="w", pady=(6, 0))
        
        # Supported formats
        formats_text = "PDF  ·  Word  ·  Excel  ·  PowerPoint  ·  Images  ·  HTML  ·  Audio  ·  EPUB"
        formats_label = ctk.CTkLabel(
            header_frame,
            text=formats_text,
            font=ctk.CTkFont(size=13),
            text_color=(COLORS["text_secondary_light"], COLORS["text_secondary_dark"])
        )
        formats_label.grid(row=2, column=0, sticky="w", pady=(12, 0))
        
    def _create_drop_zone(self):
        """Create the drag-and-drop zone."""
        self.drop_frame = ctk.CTkFrame(
            self,
            height=200,
            corner_radius=12,
            fg_color=(COLORS["surface_light"], COLORS["surface_dark_alt"]),
            border_width=2,
            border_color=(COLORS["border_light"], COLORS["border_dark"])
        )
        self.drop_frame.grid(row=1, column=0, sticky="ew", padx=48, pady=(0, 24))
        self.drop_frame.grid_columnconfigure(0, weight=1)
        self.drop_frame.grid_rowconfigure(0, weight=1)
        self.drop_frame.grid_propagate(False)
        
        # Drop zone content container
        drop_content = ctk.CTkFrame(self.drop_frame, fg_color="transparent")
        drop_content.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)
        drop_content.grid_columnconfigure(0, weight=1)
        
        # Drop text
        self.drop_label = ctk.CTkLabel(
            drop_content,
            text="Drop a file here or click to browse",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=(COLORS["text_primary_light"], COLORS["text_primary_dark"])
        )
        self.drop_label.grid(row=0, column=0, pady=(20, 4))
        
        # File name display
        self.file_label = ctk.CTkLabel(
            drop_content,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=(COLORS["accent"], COLORS["accent"])
        )
        self.file_label.grid(row=1, column=0, pady=(0, 8))
        
        # Browse button
        self.browse_btn = ctk.CTkButton(
            drop_content,
            text="Select File",
            font=ctk.CTkFont(size=15, weight="bold"),
            width=180,
            height=48,
            corner_radius=8,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color="#ffffff",
            command=self._browse_file
        )
        self.browse_btn.grid(row=2, column=0, pady=(12, 16))
        
        # Bind drag and drop
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self._on_drop)
        self.drop_frame.dnd_bind('<<DragEnter>>', self._on_drag_enter)
        self.drop_frame.dnd_bind('<<DragLeave>>', self._on_drag_leave)
        
        # Also make clicking the frame open file dialog
        self.drop_frame.bind("<Button-1>", lambda e: self._browse_file())
        
    def _create_output_area(self):
        """Create the output text area."""
        output_frame = ctk.CTkFrame(self, fg_color="transparent")
        output_frame.grid(row=2, column=0, sticky="nsew", padx=48, pady=(0, 16))
        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_rowconfigure(1, weight=1)
        
        # Output header
        output_header = ctk.CTkFrame(output_frame, fg_color="transparent")
        output_header.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        output_header.grid_columnconfigure(1, weight=1)
        
        output_label = ctk.CTkLabel(
            output_header,
            text="Output",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=(COLORS["text_primary_light"], COLORS["text_primary_dark"])
        )
        output_label.grid(row=0, column=0, sticky="w")
        
        # Status indicator
        self.status_label = ctk.CTkLabel(
            output_header,
            text="",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=(COLORS["success"], COLORS["success"])
        )
        self.status_label.grid(row=0, column=1, sticky="e")
        
        # Text output
        self.output_text = ctk.CTkTextbox(
            output_frame,
            corner_radius=10,
            font=ctk.CTkFont(family="Menlo", size=13),
            fg_color=(COLORS["surface_light"], COLORS["surface_dark"]),
            border_width=1,
            border_color=(COLORS["border_light"], COLORS["border_dark"]),
            wrap="word"
        )
        self.output_text.grid(row=1, column=0, sticky="nsew")
        self.output_text.insert("1.0", "Your converted Markdown will appear here...")
        self.output_text.configure(state="disabled", text_color=(COLORS["text_secondary_light"], COLORS["text_secondary_dark"]))
        
    def _create_footer(self):
        """Create footer with action buttons."""
        # Footer container with background
        footer_container = ctk.CTkFrame(
            self,
            fg_color=(COLORS["surface_light_alt"], COLORS["surface_dark_alt"]),
            corner_radius=0
        )
        footer_container.grid(row=3, column=0, sticky="ew")
        footer_container.grid_columnconfigure(0, weight=1)
        
        footer_frame = ctk.CTkFrame(footer_container, fg_color="transparent")
        footer_frame.grid(row=0, column=0, sticky="ew", padx=48, pady=20)
        footer_frame.grid_columnconfigure(1, weight=1)
        
        # Theme toggle (left side)
        self.theme_btn = ctk.CTkButton(
            footer_frame,
            text="Theme",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=100,
            height=48,
            corner_radius=8,
            fg_color="#374151",
            hover_color="#4b5563",
            text_color="#ffffff",
            command=self._toggle_theme
        )
        self.theme_btn.grid(row=0, column=0, sticky="w")
        
        # Button container (right aligned)
        btn_container = ctk.CTkFrame(footer_frame, fg_color="transparent")
        btn_container.grid(row=0, column=1, sticky="e")
        
        # Copy button
        self.copy_btn = ctk.CTkButton(
            btn_container,
            text="Copy",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=100,
            height=48,
            corner_radius=8,
            fg_color="#374151",
            hover_color="#4b5563",
            text_color="#ffffff",
            command=self._copy_to_clipboard,
            state="disabled"
        )
        self.copy_btn.pack(side="left", padx=(0, 12))
        
        # Save as Markdown button
        self.save_md_btn = ctk.CTkButton(
            btn_container,
            text="Save .md",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=110,
            height=48,
            corner_radius=8,
            fg_color="#374151",
            hover_color="#4b5563",
            text_color="#ffffff",
            command=self._save_markdown,
            state="disabled"
        )
        self.save_md_btn.pack(side="left", padx=(0, 12))
        
        # Save as PDF button - Primary action
        self.save_pdf_btn = ctk.CTkButton(
            btn_container,
            text="Save as PDF",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=140,
            height=48,
            corner_radius=8,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            text_color="#ffffff",
            command=self._save_pdf,
            state="disabled"
        )
        self.save_pdf_btn.pack(side="left", padx=(0, 12))
        
        # Clear button
        self.clear_btn = ctk.CTkButton(
            btn_container,
            text="Clear",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=90,
            height=48,
            corner_radius=8,
            fg_color="#dc2626",
            hover_color="#b91c1c",
            text_color="#ffffff",
            command=self._clear_all
        )
        self.clear_btn.pack(side="left")
        
    def _on_drag_enter(self, event):
        """Handle drag enter event."""
        self.drop_frame.configure(
            border_color=(COLORS["primary"], COLORS["accent"]),
            fg_color=("#eff6ff", "#1e3a5f")
        )
        self.drop_label.configure(text="Drop to convert")
        
    def _on_drag_leave(self, event):
        """Handle drag leave event."""
        self.drop_frame.configure(
            border_color=(COLORS["border_light"], COLORS["border_dark"]),
            fg_color=(COLORS["surface_light"], COLORS["surface_dark_alt"])
        )
        if not self.current_file:
            self.drop_label.configure(text="Drop a file here or click to browse")
            
    def _on_drop(self, event):
        """Handle file drop event."""
        self._on_drag_leave(event)
        
        # Parse dropped file path
        file_path = event.data
        # Handle paths with spaces (wrapped in braces on some systems)
        if file_path.startswith('{') and file_path.endswith('}'):
            file_path = file_path[1:-1]
        
        self._convert_file(file_path)
        
    def _browse_file(self):
        """Open file browser dialog."""
        file_path = filedialog.askopenfilename(
            title="Select a file to convert",
            filetypes=[
                ("All Supported", "*.pdf *.docx *.doc *.xlsx *.xls *.pptx *.ppt *.html *.htm *.csv *.json *.xml *.jpg *.jpeg *.png *.gif *.mp3 *.wav *.epub *.zip *.md *.markdown *.txt *.rtf"),
                ("Markdown", "*.md *.markdown"),
                ("PDF Files", "*.pdf"),
                ("Word Documents", "*.docx *.doc"),
                ("Excel Files", "*.xlsx *.xls"),
                ("PowerPoint", "*.pptx *.ppt"),
                ("Web Files", "*.html *.htm"),
                ("Text Files", "*.txt *.rtf"),
                ("Data Files", "*.csv *.json *.xml"),
                ("Images", "*.jpg *.jpeg *.png *.gif"),
                ("Audio", "*.mp3 *.wav"),
                ("EPUB", "*.epub"),
                ("ZIP Archives", "*.zip"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            self._convert_file(file_path)
            
    def _convert_file(self, file_path: str):
        """Convert the given file to Markdown."""
        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"File not found: {file_path}")
            return
            
        self.current_file = file_path
        file_name = os.path.basename(file_path)
        file_ext = Path(file_path).suffix.lower()
        
        # Update UI
        self.drop_label.configure(text="Converting...")
        self.file_label.configure(text=file_name)
        self.status_label.configure(text="Processing", text_color=(COLORS["warning"], COLORS["warning"]))
        
        # Disable buttons during conversion
        self.browse_btn.configure(state="disabled")
        self.copy_btn.configure(state="disabled")
        self.save_md_btn.configure(state="disabled")
        self.save_pdf_btn.configure(state="disabled")
        
        # Check if it's already a markdown file - just read it directly
        if file_ext in ['.md', '.markdown']:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.converted_content = f.read()
                self._conversion_complete(True)
            except Exception as e:
                self._conversion_complete(False, str(e))
        else:
            # Run conversion in background thread
            thread = threading.Thread(target=self._do_conversion, args=(file_path,))
            thread.daemon = True
            thread.start()
        
    def _do_conversion(self, file_path: str):
        """Perform the actual conversion (runs in background thread)."""
        try:
            result = self.md.convert(file_path)
            self.converted_content = result.text_content
            
            # Update UI on main thread
            self.after(0, lambda: self._conversion_complete(True))
            
        except Exception as e:
            error_msg = str(e)
            self.after(0, lambda: self._conversion_complete(False, error_msg))
            
    def _conversion_complete(self, success: bool, error_msg: str = None):
        """Handle conversion completion (runs on main thread)."""
        self.browse_btn.configure(state="normal")
        
        if success:
            self.drop_label.configure(text="Conversion complete")
            self.status_label.configure(text="Ready", text_color=(COLORS["success"], COLORS["success"]))
            
            # Update output text
            self.output_text.configure(state="normal", text_color=(COLORS["text_primary_light"], COLORS["text_primary_dark"]))
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", self.converted_content)
            self.output_text.configure(state="disabled")
            
            # Enable action buttons
            self.copy_btn.configure(state="normal")
            self.save_md_btn.configure(state="normal")
            if HAS_PDF_EXPORT:
                self.save_pdf_btn.configure(state="normal")
            
        else:
            self.drop_label.configure(text="Conversion failed")
            self.status_label.configure(text="Error", text_color=(COLORS["error"], COLORS["error"]))
            
            self.output_text.configure(state="normal", text_color=(COLORS["error"], COLORS["error"]))
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", f"Error converting file:\n\n{error_msg}")
            self.output_text.configure(state="disabled")
            
    def _copy_to_clipboard(self):
        """Copy converted content to clipboard."""
        if self.converted_content:
            self.clipboard_clear()
            self.clipboard_append(self.converted_content)
            
            # Show feedback
            original_text = self.copy_btn.cget("text")
            self.copy_btn.configure(text="Copied")
            self.after(1500, lambda: self.copy_btn.configure(text=original_text))
            
    def _save_markdown(self):
        """Save converted content as Markdown file."""
        if not self.converted_content:
            return
            
        # Generate default filename
        if self.current_file:
            default_name = Path(self.current_file).stem + ".md"
        else:
            default_name = "converted.md"
            
        file_path = filedialog.asksaveasfilename(
            title="Save Markdown file",
            defaultextension=".md",
            initialfile=default_name,
            filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.converted_content)
                    
                # Show feedback
                original_text = self.save_md_btn.cget("text")
                self.save_md_btn.configure(text="Saved")
                self.after(1500, lambda: self.save_md_btn.configure(text=original_text))
                
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save file:\n{str(e)}")
    
    def _save_pdf(self):
        """Save converted content as PDF file."""
        if not self.converted_content:
            return
            
        if not HAS_PDF_EXPORT:
            messagebox.showerror("PDF Export Unavailable", "PDF export requires additional libraries.\nInstall: pip install markdown weasyprint")
            return
            
        # Generate default filename
        if self.current_file:
            default_name = Path(self.current_file).stem + ".pdf"
        else:
            default_name = "converted.pdf"
            
        file_path = filedialog.asksaveasfilename(
            title="Save PDF file",
            defaultextension=".pdf",
            initialfile=default_name,
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        
        if file_path:
            # Update status
            original_text = self.save_pdf_btn.cget("text")
            self.save_pdf_btn.configure(text="Exporting...", state="disabled")
            
            # Run PDF export in background
            thread = threading.Thread(target=self._do_pdf_export, args=(file_path, original_text))
            thread.daemon = True
            thread.start()
    
    def _do_pdf_export(self, file_path: str, original_btn_text: str):
        """Perform PDF export (runs in background thread)."""
        try:
            # Convert Markdown to HTML
            md_converter = markdown.Markdown(
                extensions=['tables', 'fenced_code', 'codehilite', 'toc', 'nl2br']
            )
            html_content = md_converter.convert(self.converted_content)
            
            # Wrap in full HTML document
            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Document</title>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """
            
            # Convert HTML to PDF
            html_doc = HTML(string=full_html)
            css = CSS(string=PDF_CSS)
            html_doc.write_pdf(file_path, stylesheets=[css])
            
            # Update UI on main thread
            self.after(0, lambda: self._pdf_export_complete(True, original_btn_text))
            
        except Exception as e:
            error_msg = str(e)
            self.after(0, lambda: self._pdf_export_complete(False, original_btn_text, error_msg))
    
    def _pdf_export_complete(self, success: bool, original_btn_text: str, error_msg: str = None):
        """Handle PDF export completion."""
        self.save_pdf_btn.configure(state="normal")
        
        if success:
            self.save_pdf_btn.configure(text="Saved")
            self.after(1500, lambda: self.save_pdf_btn.configure(text=original_btn_text))
        else:
            self.save_pdf_btn.configure(text=original_btn_text)
            messagebox.showerror("PDF Export Error", f"Could not export PDF:\n{error_msg}")
                
    def _clear_all(self):
        """Clear the current file and output."""
        self.current_file = None
        self.converted_content = None
        
        # Reset drop zone
        self.drop_label.configure(text="Drop a file here or click to browse")
        self.file_label.configure(text="")
        
        # Reset output
        self.output_text.configure(state="normal", text_color=(COLORS["text_secondary_light"], COLORS["text_secondary_dark"]))
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", "Your converted Markdown will appear here...")
        self.output_text.configure(state="disabled")
        
        # Reset status
        self.status_label.configure(text="")
        
        # Disable buttons
        self.copy_btn.configure(state="disabled")
        self.save_md_btn.configure(state="disabled")
        self.save_pdf_btn.configure(state="disabled")
        
    def _toggle_theme(self):
        """Toggle between light and dark theme."""
        current = ctk.get_appearance_mode()
        if current == "Dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")


def main():
    """Run the application."""
    app = MarkItDownApp()
    app.mainloop()


if __name__ == "__main__":
    main()
