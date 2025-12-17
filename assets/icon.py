#!/usr/bin/env python3
"""
Generate app icon for MarkItDown.
Creates PNG and ICNS (Mac) / ICO (Windows) icons.
"""

import os
from pathlib import Path

# Try to import PIL for icon generation
try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Note: Install Pillow for icon generation: pip install Pillow")


def create_icon():
    """Create the app icon programmatically."""
    if not HAS_PIL:
        print("Pillow not installed. Skipping icon generation.")
        return None
    
    # Create a 1024x1024 icon (will be scaled down)
    size = 1024
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background - rounded rectangle with gradient effect
    # Primary color: Deep indigo #4f46e5
    padding = 80
    corner_radius = 200
    
    # Draw rounded rectangle background
    draw.rounded_rectangle(
        [(padding, padding), (size - padding, size - padding)],
        radius=corner_radius,
        fill='#4f46e5'
    )
    
    # Add a subtle gradient overlay (lighter at top)
    for i in range(100):
        alpha = int(30 * (1 - i / 100))
        y = padding + i * 2
        if y < size // 2:
            draw.rectangle(
                [(padding + corner_radius // 2, y), 
                 (size - padding - corner_radius // 2, y + 2)],
                fill=(255, 255, 255, alpha)
            )
    
    # Draw markdown icon (stylized "MD" or document icon)
    # Document shape
    doc_left = 280
    doc_top = 200
    doc_right = 744
    doc_bottom = 824
    fold_size = 120
    
    # Document with folded corner
    doc_points = [
        (doc_left, doc_top + fold_size),
        (doc_left + fold_size, doc_top),
        (doc_right, doc_top),
        (doc_right, doc_bottom),
        (doc_left, doc_bottom),
    ]
    draw.polygon(doc_points, fill='white')
    
    # Fold triangle
    fold_points = [
        (doc_left, doc_top + fold_size),
        (doc_left + fold_size, doc_top + fold_size),
        (doc_left + fold_size, doc_top),
    ]
    draw.polygon(fold_points, fill='#c7d2fe')
    
    # Draw "MD" text or markdown symbol
    # Using lines to represent text
    line_color = '#4f46e5'
    line_y_start = 380
    line_height = 50
    line_spacing = 30
    
    for i in range(5):
        y = line_y_start + i * (line_height + line_spacing)
        # Vary line lengths
        if i == 0:
            width_pct = 0.8
        elif i == 1:
            width_pct = 0.95
        elif i == 2:
            width_pct = 0.6
        elif i == 3:
            width_pct = 0.85
        else:
            width_pct = 0.5
            
        line_width = int((doc_right - doc_left - 100) * width_pct)
        draw.rounded_rectangle(
            [(doc_left + 50, y), (doc_left + 50 + line_width, y + line_height)],
            radius=10,
            fill=line_color
        )
    
    # Save the icon
    assets_dir = Path(__file__).parent
    
    # Save as PNG
    png_path = assets_dir / 'icon.png'
    img.save(png_path, 'PNG')
    print(f"Created: {png_path}")
    
    # Create different sizes for .icns
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    icon_images = []
    for s in sizes:
        resized = img.resize((s, s), Image.Resampling.LANCZOS)
        icon_images.append(resized)
    
    # Save as .ico (Windows)
    ico_path = assets_dir / 'icon.ico'
    icon_images[0].save(
        ico_path, 
        format='ICO', 
        sizes=[(s, s) for s in [16, 32, 48, 64, 128, 256]]
    )
    print(f"Created: {ico_path}")
    
    return png_path


def create_icns_from_png(png_path):
    """Create macOS .icns file from PNG (requires iconutil on macOS)."""
    import subprocess
    import tempfile
    import shutil
    
    if not HAS_PIL:
        return None
        
    png_path = Path(png_path)
    assets_dir = png_path.parent
    
    # Create iconset directory
    with tempfile.TemporaryDirectory() as tmpdir:
        iconset_path = Path(tmpdir) / 'icon.iconset'
        iconset_path.mkdir()
        
        img = Image.open(png_path)
        
        # Generate all required sizes
        icon_sizes = [
            (16, '16x16'),
            (32, '16x16@2x'),
            (32, '32x32'),
            (64, '32x32@2x'),
            (128, '128x128'),
            (256, '128x128@2x'),
            (256, '256x256'),
            (512, '256x256@2x'),
            (512, '512x512'),
            (1024, '512x512@2x'),
        ]
        
        for size, name in icon_sizes:
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            resized.save(iconset_path / f'icon_{name}.png')
        
        # Use iconutil to create .icns
        icns_path = assets_dir / 'icon.icns'
        try:
            subprocess.run(
                ['iconutil', '-c', 'icns', str(iconset_path), '-o', str(icns_path)],
                check=True
            )
            print(f"Created: {icns_path}")
            return icns_path
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Note: iconutil not available (macOS only)")
            return None


if __name__ == '__main__':
    png = create_icon()
    if png:
        create_icns_from_png(png)

