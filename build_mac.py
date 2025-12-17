#!/usr/bin/env python3
"""
Build script for macOS .app bundle.
Creates a standalone MarkItDown application.
"""

import os
import sys
import subprocess
from pathlib import Path

# Project paths
PROJECT_DIR = Path(__file__).parent
ASSETS_DIR = PROJECT_DIR / 'assets'
DIST_DIR = PROJECT_DIR / 'dist'
BUILD_DIR = PROJECT_DIR / 'build'

APP_NAME = 'MarkItDown'
MAIN_SCRIPT = PROJECT_DIR / 'app.py'


def generate_icons():
    """Generate app icons if they don't exist."""
    icon_png = ASSETS_DIR / 'icon.png'
    icon_icns = ASSETS_DIR / 'icon.icns'
    
    if not icon_png.exists():
        print("Generating icons...")
        try:
            from assets.icon import create_icon, create_icns_from_png
            png = create_icon()
            if png:
                create_icns_from_png(png)
        except ImportError:
            print("Note: Could not generate icons. Install Pillow: pip install Pillow")
    
    return icon_icns if icon_icns.exists() else None


def build_with_pyinstaller():
    """Build using PyInstaller."""
    icon_path = generate_icons()
    
    # PyInstaller command
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--name', APP_NAME,
        '--windowed',  # No console window
        '--onedir',    # Create a directory with all files
        '--clean',     # Clean cache
        '--noconfirm', # Overwrite without asking
    ]
    
    # Add icon if available
    if icon_path and icon_path.exists():
        cmd.extend(['--icon', str(icon_path)])
    
    # Add hidden imports that PyInstaller might miss
    hidden_imports = [
        'markitdown',
        'customtkinter',
        'tkinterdnd2',
        'PIL',
        'PIL.Image',
        'pdfminer',
        'pdfminer.high_level',
        'docx',
        'pptx',
        'openpyxl',
        'xlrd',
        'bs4',
        'lxml',
        'charset_normalizer',
        'magika',
        'markdown',
        'weasyprint',
    ]
    
    for imp in hidden_imports:
        cmd.extend(['--hidden-import', imp])
    
    # Collect data for customtkinter and magika (models)
    cmd.extend(['--collect-data', 'customtkinter'])
    cmd.extend(['--collect-data', 'magika'])
    
    # Add the main script
    cmd.append(str(MAIN_SCRIPT))
    
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    
    print(f"\n✅ Build complete!")
    print(f"App location: {DIST_DIR / APP_NAME}.app")


def main():
    os.chdir(PROJECT_DIR)
    
    print("=" * 50)
    print("MarkItDown macOS Build")
    print("=" * 50)
    
    # Check for required packages
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
    
    build_with_pyinstaller()


if __name__ == '__main__':
    main()

