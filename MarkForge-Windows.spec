# -*- mode: python ; coding: utf-8 -*-
# MarkForge Desktop App - Windows PyInstaller Spec File

from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os

# Get project directory
project_dir = os.path.dirname(os.path.abspath(SPEC))

# Collect all data files
datas = []
datas += collect_data_files('markitdown')
datas += collect_data_files('magika')
datas += [(os.path.join(project_dir, 'templates'), 'templates')]

# Collect hidden imports
hiddenimports = collect_submodules('markitdown')
hiddenimports += collect_submodules('webview')
hiddenimports += [
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
    'clr',
    'pythonnet',
]

a = Analysis(
    [os.path.join(project_dir, 'app.py')],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['weasyprint', 'cairocffi', 'tinycss2', 'cssselect2', 'pyphen', 'playwright'],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MarkForge',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(project_dir, 'assets', 'icon.ico'),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MarkForge',
)

