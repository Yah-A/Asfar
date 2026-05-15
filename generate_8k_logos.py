#!/usr/bin/env python3
"""
Generate 8K resolution versions of the Asfar logo
- Square version (8192x8192)
- Circular version with transparent background
"""

import subprocess
import os
from PIL import Image, ImageDraw

# Directories
OUTPUT_DIR = "/workspace/assets/images"
SVG_PATH = "/workspace/assets/images/asfar-logo.svg"

# 8K resolution (using 8192 for true square 8K)
SIZE_8K = 8192

def svg_to_png_rsvg(svg_path, png_path, size):
    """Convert SVG to PNG at specified size using rsvg-convert"""
    cmd = [
        "rsvg-convert",
        "-w", str(size),
        "-h", str(size),
        "-o", png_path,
        svg_path
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    print(f"Created: {png_path}")

def create_square_8k():
    """Create 8K square version"""
    output_path = os.path.join(OUTPUT_DIR, "asfar-logo-8k-square.png")
    svg_to_png_rsvg(SVG_PATH, output_path, SIZE_8K)
    return output_path

def create_circular_8k(square_path):
    """Create 8K circular version with transparent background outside circle"""
    # Open the square image
    img = Image.open(square_path).convert("RGBA")
    
    # Create circular mask
    size = img.size[0]
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    
    # Apply mask to create circular image
    output = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    output.paste(img, (0, 0), mask)
    
    # Save circular version
    output_path = os.path.join(OUTPUT_DIR, "asfar-logo-8k-circle.png")
    output.save(output_path, "PNG")
    print(f"Created: {output_path}")
    
    return output_path

def main():
    print("=" * 50)
    print("Generating 8K Asfar Logo Versions")
    print("=" * 50)
    print(f"Resolution: {SIZE_8K}x{SIZE_8K} pixels")
    print()
    
    # Create output directory if needed
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Generate square version
    print("1. Creating 8K Square Version...")
    square_path = create_square_8k()
    
    # Get file info for square
    if os.path.exists(square_path):
        img = Image.open(square_path)
        print(f"   Dimensions: {img.size[0]}x{img.size[1]} pixels")
        size_mb = os.path.getsize(square_path) / (1024 * 1024)
        print(f"   File size: {size_mb:.2f} MB")
    
    # Generate circular version
    print("\n2. Creating 8K Circular Version...")
    circle_path = create_circular_8k(square_path)
    
    # Get file info for circle
    if os.path.exists(circle_path):
        img = Image.open(circle_path)
        print(f"   Dimensions: {img.size[0]}x{img.size[1]} pixels")
        size_mb = os.path.getsize(circle_path) / (1024 * 1024)
        print(f"   File size: {size_mb:.2f} MB")
    
    print("\n" + "=" * 50)
    print("Generation Complete!")
    print("=" * 50)
    print(f"\nFiles created in: {OUTPUT_DIR}")
    print(f"  - asfar-logo-8k-square.png  (Square 8K)")
    print(f"  - asfar-logo-8k-circle.png  (Circular 8K)")

if __name__ == "__main__":
    main()
