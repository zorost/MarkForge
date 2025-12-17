#!/usr/bin/env python3
"""
Setup script for MarkItDown Desktop App.
Installs all dependencies and optionally generates icons.
"""

import subprocess
import sys
from pathlib import Path


def main():
    print("=" * 50)
    print("MarkItDown Desktop App - Setup")
    print("=" * 50)
    print()
    
    # Step 1: Create virtual environment if it doesn't exist
    venv_path = Path(__file__).parent / '.venv'
    
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', str(venv_path)], check=True)
        print("   ✓ Virtual environment created")
    else:
        print("📦 Virtual environment already exists")
    
    # Determine pip path
    if sys.platform == 'win32':
        pip_path = venv_path / 'Scripts' / 'pip'
        python_path = venv_path / 'Scripts' / 'python'
    else:
        pip_path = venv_path / 'bin' / 'pip'
        python_path = venv_path / 'bin' / 'python'
    
    # Step 2: Upgrade pip
    print("\n📦 Upgrading pip...")
    subprocess.run([str(pip_path), 'install', '--upgrade', 'pip'], check=True)
    
    # Step 3: Install requirements
    print("\n📦 Installing dependencies...")
    requirements_path = Path(__file__).parent / 'requirements.txt'
    subprocess.run([str(pip_path), 'install', '-r', str(requirements_path)], check=True)
    print("   ✓ Dependencies installed")
    
    # Step 4: Generate icons (optional)
    print("\n🎨 Generating app icons...")
    try:
        subprocess.run([str(pip_path), 'install', 'Pillow'], check=True)
        icon_script = Path(__file__).parent / 'assets' / 'icon.py'
        subprocess.run([str(python_path), str(icon_script)], check=True)
    except Exception as e:
        print(f"   Note: Could not generate icons ({e})")
    
    print("\n" + "=" * 50)
    print("✅ Setup complete!")
    print("=" * 50)
    print()
    print("To run the app:")
    print()
    
    if sys.platform == 'win32':
        print(f"  1. Activate: .venv\\Scripts\\activate")
    else:
        print(f"  1. Activate: source .venv/bin/activate")
    
    print("  2. Run: python app.py")
    print()
    print("To build a standalone app:")
    print()
    
    if sys.platform == 'darwin':
        print("  python build_mac.py")
    else:
        print("  python build_windows.py")
    print()


if __name__ == '__main__':
    main()

