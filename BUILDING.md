# Building MarkForge Desktop Applications

This guide provides detailed instructions for building MarkForge desktop applications for macOS and Windows.

---

## Prerequisites

### All Platforms

- Python 3.10 or higher
- Git
- Internet connection (for downloading dependencies)

### macOS

- macOS 10.15 (Catalina) or later
- Xcode Command Line Tools (`xcode-select --install`)

### Windows

- Windows 10 or later
- .NET Framework 4.6.2 or later (usually pre-installed)
- Microsoft Visual C++ Redistributable (for some dependencies)

---

## Building for macOS

### Step 1: Clone and Setup

```bash
git clone https://github.com/zorost/MarkForge.git
cd MarkForge

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install pywebview pyinstaller
```

### Step 2: Build the Application

```bash
python build_mac.py
```

This will:
- Build the application using PyInstaller
- Create `dist/MarkForge.app`
- Automatically install to `/Applications/MarkForge.app`

### Step 3: Create Distribution Package

```bash
cd dist
zip -r MarkForge-macOS.zip MarkForge.app
```

---

## Building for Windows

### Step 1: Clone and Setup

Open PowerShell or Command Prompt:

```powershell
git clone https://github.com/zorost/MarkForge.git
cd MarkForge

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install pywebview pyinstaller pythonnet
```

### Step 2: Build the Application

```powershell
python build_windows.py
```

Or use PyInstaller directly:

```powershell
pyinstaller --clean MarkForge-Windows.spec
```

This will create the executable at `dist\MarkForge\MarkForge.exe`.

### Step 3: Create Distribution Package

```powershell
# Create zip archive
Compress-Archive -Path dist\MarkForge -DestinationPath MarkForge-Windows.zip
```

---

## Build Output

| Platform | Output Location | Package Name |
|----------|-----------------|--------------|
| macOS | `dist/MarkForge.app` | `MarkForge-macOS.zip` |
| Windows | `dist/MarkForge/MarkForge.exe` | `MarkForge-Windows.zip` |

---

## Troubleshooting

### macOS

**Issue: "App is damaged" warning**
```bash
xattr -cr /Applications/MarkForge.app
```

**Issue: Build fails with missing modules**
```bash
pip install --upgrade pyinstaller
pip install pyobjc-core pyobjc-framework-Cocoa pyobjc-framework-WebKit
```

### Windows

**Issue: Missing DLL errors**
- Install Microsoft Visual C++ Redistributable 2015-2022
- Ensure .NET Framework 4.6.2+ is installed

**Issue: PyWebView not working**
```powershell
pip install pythonnet
pip install --upgrade pywebview
```

**Issue: Build fails with encoding errors**
- Ensure your terminal is using UTF-8 encoding
- Set environment variable: `$env:PYTHONUTF8=1`

---

## Development Notes

### Architecture

The desktop application uses:
- **Flask** - Web server running locally
- **pywebview** - Native window wrapper around the web UI
- **PyInstaller** - Packages everything into a standalone executable

### Key Files

| File | Description |
|------|-------------|
| `app.py` | Desktop application entry point |
| `server.py` | Flask web server with conversion APIs |
| `templates/index.html` | Main web UI |
| `MarkForge.spec` | PyInstaller spec for macOS |
| `MarkForge-Windows.spec` | PyInstaller spec for Windows |
| `build_mac.py` | macOS build script |
| `build_windows.py` | Windows build script |

---

## Contributing Builds

If you build a Windows version, we welcome contributions:

1. Build using the instructions above
2. Test the application thoroughly
3. Create a GitHub Issue or Pull Request with the build artifact
4. Or contact us at [zorost.com](https://zorost.com)

---

Developed by **Zorost Intelligence**

