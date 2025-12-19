# -*- mode: python ; coding: utf-8 -*-
# MarkForge Desktop App - PyInstaller Spec File

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all data files
datas = []
datas += collect_data_files('markitdown')
datas += collect_data_files('magika')
datas += collect_data_files('xhtml2pdf')
datas += collect_data_files('reportlab')

# Add templates folder
datas += [('/Users/eloy/Desktop/BIZ 2025/Zorost/Projects/Zorost-APPS/MarkitDown/MarkitDown-App/templates', 'templates')]

# Collect hidden imports
hiddenimports = collect_submodules('markitdown')
hiddenimports += collect_submodules('webview')
hiddenimports += collect_submodules('xhtml2pdf')
hiddenimports += collect_submodules('reportlab')
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
    'pyobjc',
    # xhtml2pdf and dependencies for PDF generation
    'xhtml2pdf',
    'xhtml2pdf.pisa',
    'xhtml2pdf.context',
    'xhtml2pdf.parser',
    'xhtml2pdf.w3c',
    'xhtml2pdf.default',
    'reportlab',
    'reportlab.graphics',
    'reportlab.graphics.barcode',
    'reportlab.lib',
    'reportlab.pdfbase',
    'reportlab.pdfgen',
    'reportlab.platypus',
    'svglib',
    'svglib.svglib',
    'arabic_reshaper',
    'html5lib',
    'pypdf',
]

a = Analysis(
    ['/Users/eloy/Desktop/BIZ 2025/Zorost/Projects/Zorost-APPS/MarkitDown/MarkitDown-App/app.py'],
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
    icon=['/Users/eloy/Desktop/BIZ 2025/Zorost/Projects/Zorost-APPS/MarkitDown/MarkitDown-App/assets/icon.icns'],
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

app = BUNDLE(
    coll,
    name='MarkForge.app',
    icon='/Users/eloy/Desktop/BIZ 2025/Zorost/Projects/Zorost-APPS/MarkitDown/MarkitDown-App/assets/icon.icns',
    bundle_identifier='com.zorost.markforge',
    info_plist={
        'CFBundleName': 'MarkForge',
        'CFBundleDisplayName': 'MarkForge',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13.0',
    },
)
