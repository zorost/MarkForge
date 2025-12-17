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

# Add the current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask server
from server import app as flask_app


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
    
    # Create the desktop window with the web UI
    window = webview.create_window(
        title='MarkForge - Document Converter',
        url='http://127.0.0.1:7862',
        width=1280,
        height=850,
        min_size=(900, 600),
        resizable=True,
        background_color='#020617',  # Dark background
        text_select=True,
    )
    
    # Start the webview (this blocks until window is closed)
    webview.start()


if __name__ == '__main__':
    main()
