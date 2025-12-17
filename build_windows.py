#!/usr/bin/env python3
"""
MarkForge - Windows Build Script
Builds the desktop application for Windows using PyInstaller.
Run this script on a Windows machine.
"""

import os
import sys
import subprocess
from pathlib import Path

# Project paths
PROJECT_DIR = Path(__file__).parent
ASSETS_DIR = PROJECT_DIR / 'assets'
DIST_DIR = PROJECT_DIR / 'dist'

APP_NAME = 'MarkForge'
MAIN_SCRIPT = PROJECT_DIR / 'app.py'


def build():
    """Build MarkForge for Windows."""
    os.chdir(PROJECT_DIR)
    
    print("=" * 60)
    print("Building MarkForge for Windows...")
    print("=" * 60)
    
    # Check for required packages
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
    
    # Icon path
    icon_path = ASSETS_DIR / 'icon.ico'
    
    # PyInstaller command
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--name', APP_NAME,
        '--windowed',  # No console window
        '--clean',
        '--noconfirm',
    ]
    
    # Add icon
    if icon_path.exists():
        cmd.extend(['--icon', str(icon_path)])
    
    # Add templates folder
    cmd.extend(['--add-data', f'{PROJECT_DIR / "templates"};templates'])
    
    # Collect data files
    cmd.extend(['--collect-data', 'markitdown'])
    cmd.extend(['--collect-data', 'magika'])
    
    # Hidden imports
    hidden_imports = [
        'webview',
        'flask',
        'markdown',
        'markitdown',
        'PIL',
        'PIL.Image',
        'pdfminer',
        'pdfminer.high_level',
        'pptx',
        'openpyxl',
        'bs4',
        'lxml',
        'charset_normalizer',
        'magika',
        'bottle',
        'clr',  # pythonnet for Windows webview
    ]
    
    for imp in hidden_imports:
        cmd.extend(['--hidden-import', imp])
    
    # Exclude heavy/problematic packages
    excludes = ['playwright', 'weasyprint', 'cairocffi', 'tinycss2']
    for exc in excludes:
        cmd.extend(['--exclude-module', exc])
    
    # Add main script
    cmd.append(str(MAIN_SCRIPT))
    
    print(f"\nRunning PyInstaller...")
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("✅ Build successful!")
        print(f"Executable: {DIST_DIR / APP_NAME / APP_NAME}.exe")
        print("=" * 60)
    else:
        print("\n❌ Build failed!")
        sys.exit(1)


if __name__ == '__main__':
    build()
