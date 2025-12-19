#!/usr/bin/env python3
"""
MarkForge Desktop App
A professional document converter by Zorost Intelligence.
Powered by Microsoft's MarkItDown library.

This desktop app wraps the web UI for a native experience.
"""

import webview
import threading
import sys
import os
import base64
import tempfile

# Add the current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask server
from server import app as flask_app


class Api:
    """API class for JS-Python bridge to handle file operations."""
    
    def __init__(self):
        self._window = None
    
    def set_window(self, window):
        """Set the window reference after creation."""
        self._window = window
    
    def save_file(self, content_b64, filename, file_type):
        """Save file using native file dialog.
        
        Args:
            content_b64: Base64 encoded file content
            filename: Suggested filename
            file_type: MIME type (e.g., 'application/pdf', 'text/markdown')
        """
        try:
            if not self._window:
                return {'success': False, 'error': 'Window not initialized'}
            
            # Decode base64 content
            content = base64.b64decode(content_b64)
            
            # Determine file extension
            if file_type == 'application/pdf':
                default_ext = '.pdf'
            elif file_type == 'text/markdown':
                default_ext = '.md'
            elif file_type == 'text/plain':
                default_ext = '.txt'
            else:
                default_ext = ''
            
            # Get default directory (user's Downloads or Documents folder)
            default_dir = os.path.expanduser('~/Downloads')
            if not os.path.exists(default_dir):
                default_dir = os.path.expanduser('~/Documents')
            if not os.path.exists(default_dir):
                default_dir = os.path.expanduser('~')
            
            # Show save dialog
            save_path = self._window.create_file_dialog(
                webview.SAVE_DIALOG,
                directory=default_dir,
                save_filename=filename
            )
            
            if save_path:
                # save_path can be a string or tuple
                if isinstance(save_path, (list, tuple)):
                    save_path = save_path[0] if save_path else None
                
                if save_path:
                    # Ensure correct extension
                    if default_ext and not save_path.lower().endswith(default_ext):
                        save_path += default_ext
                    
                    # Write file
                    with open(save_path, 'wb') as f:
                        f.write(content)
                    
                    return {'success': True, 'path': save_path}
            
            return {'success': False, 'error': 'Save cancelled'}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}


def start_server():
    """Start the Flask server in a background thread."""
    flask_app.run(host='127.0.0.1', port=7862, debug=False, use_reloader=False)


def main():
    """Launch the MarkForge desktop application."""
    # Start Flask server in background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Give server a moment to start
    import time
    time.sleep(1)
    
    # Create API instance first
    api = Api()
    
    # Create the desktop window with the web UI and expose the API
    window = webview.create_window(
        title='MarkForge - Document Converter',
        url='http://127.0.0.1:7862',
        width=1280,
        height=850,
        min_size=(900, 600),
        resizable=True,
        background_color='#020617',  # Dark background
        text_select=True,
        js_api=api,  # Expose API to JavaScript as window.pywebview.api
    )
    
    # Set window reference in API
    api.set_window(window)
    
    # Start the webview
    webview.start(private_mode=False)


if __name__ == '__main__':
    main()
