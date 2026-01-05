from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

# Target Directory (Relative to this script)
# Script is in ./scripts/, so we go up one level to root, then to frontend/assets
ASSETS_DIR = Path(__file__).parent.parent / "frontend" / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

def create_clarity_logo():
    # 1. Setup - 1024x1024 Canvas
    size = 1024
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 2. Colors (Catppuccin Mocha)
    base = "#1e1e2e"
    lavender = "#b4befe" # Primary Brand Color
    teal = "#94e2d5"     # Accent
    crust = "#11111b"

    # 3. Geometry - The "Lens" / "Focus" Concept
    # A central circle (the lens) with a bracket frame
    
    padding = 100
    center = size // 2
    
    # Outer container (optional, maybe just the symbol)
    # Let's draw a thick ring (The "Clarity" circle)
    ring_width = 120
    bbox = [padding, padding, size-padding, size-padding]
    
    # Draw base ring
    draw.ellipse(bbox, outline=lavender, width=ring_width)
    
    # 4. The "Code" Cut
    # We want it to look like code brackets `< >` or a focused lens.
    # Let's slice the top and bottom to make it look like two parenthesis ()
    
    # Masking rects at top and bottom
    cut_height = 200
    cut_width = 150
    
    # Top cut
    draw.rectangle(
        [(center - cut_width, 0), (center + cut_width, padding + ring_width + 50)],
        fill=(0,0,0,0) # This draws transparent on RGBA? No, it draws black/transparent color. 
                       # PIL draw doesn't "erase" easily without composition.
    )
    # Actually, simpler to draw two arcs.
    
    # Reset and draw arcs instead
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Left Bracket (Cyan/Teal)
    draw.arc(bbox, start=110, end=250, fill=teal, width=ring_width)
    
    # Right Bracket (Lavender)
    draw.arc(bbox, start=290, end=430, fill=lavender, width=ring_width)
    
    # 5. The Core (The "Correct" Code)
    # A solid dot or checkmark in the center
    core_size = 180
    core_bbox = [center-core_size, center-core_size, center+core_size, center+core_size]
    draw.ellipse(core_bbox, fill=lavender)
    
    # 6. Save
    output_path = ASSETS_DIR / "logo.png"
    img.save(output_path, "PNG")
    print(f"Clarity Logo generated at {output_path}")

def create_overai_logo():
    # 1. Setup - 1024x1024 Canvas
    size = 1024
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 2. Colors (Catppuccin Mocha)
    lavender = "#b4befe" 
    teal = "#94e2d5"
    
    # 3. Geometry - Minimalist "Chevron & Foundation"
    # A theoretical diamond split in two.
    
    center_x = size // 2
    center_y = size // 2
    
    # Dimensions
    # Total height of the "logo mark" roughly 700px
    # Half height ~350
    # Width ~700
    
    # Gap between the top chevron and bottom triangle
    gap = 40
    
    # BOTTOM: Solid Teal Triangle
    # It's the bottom half of a diamond.
    # Vertices: Left, Right, Bottom
    # Let's say the "equator" is slightly below center to account for visual weight
    equator_y = center_y + (gap // 2)
    
    triangle_width_half = 350
    triangle_height = 350
    
    bottom_triangle_coords = [
        (center_x - triangle_width_half, equator_y), # Top Left of triangle
        (center_x + triangle_width_half, equator_y), # Top Right of triangle
        (center_x, equator_y + triangle_height)      # Bottom Tip
    ]
    draw.polygon(bottom_triangle_coords, fill=teal)
    
    # TOP: Lavender Chevron (Thick Line)
    # It's the top half of the diamond, but just the "roof"
    # Vertices for the chevron path: Left -> Top -> Right
    
    chevron_bottom_y = center_y - (gap // 2)
    chevron_top_y = chevron_bottom_y - triangle_height
    
    # We want the chevron to align with the triangle's width at the bottom
    chevron_coords = [
        (center_x - triangle_width_half, chevron_bottom_y), # Bottom Left
        (center_x, chevron_top_y),                         # Top Tip
        (center_x + triangle_width_half, chevron_bottom_y)  # Bottom Right
    ]
    
    draw.line(chevron_coords, fill=lavender, width=80, joint="curve")
    
    # 4. Save
    output_path = ASSETS_DIR / "overai_logo.png"
    img.save(output_path, "PNG")
    print(f"OverAI Logo generated at {output_path}")

def create_overai_logo_bg():
    # 1. Setup - 1024x1024 Canvas with Catppuccin Base Background
    size = 1024
    base_color = "#1e1e2e"
    img = Image.new('RGB', (size, size), base_color)
    draw = ImageDraw.Draw(img)

    # 2. Colors
    lavender = "#b4befe" 
    teal = "#94e2d5"
    
    # 3. Geometry - Minimalist "Chevron & Foundation"
    center_x = size // 2
    center_y = size // 2
    gap = 40
    
    # BOTTOM: Solid Teal Triangle
    equator_y = center_y + (gap // 2)
    triangle_width_half = 350
    triangle_height = 350
    
    bottom_triangle_coords = [
        (center_x - triangle_width_half, equator_y), 
        (center_x + triangle_width_half, equator_y), 
        (center_x, equator_y + triangle_height)      
    ]
    draw.polygon(bottom_triangle_coords, fill=teal)
    
    # TOP: Lavender Chevron
    chevron_bottom_y = center_y - (gap // 2)
    chevron_top_y = chevron_bottom_y - triangle_height
    chevron_coords = [
        (center_x - triangle_width_half, chevron_bottom_y), 
        (center_x, chevron_top_y),                         
        (center_x + triangle_width_half, chevron_bottom_y)  
    ]
    draw.line(chevron_coords, fill=lavender, width=80, joint="curve")
    
    # 4. Save
    output_path = ASSETS_DIR / "overai_logo_bg.png"
    img.save(output_path, "PNG")
    print(f"OverAI Logo with background generated at {output_path}")

if __name__ == "__main__":
    create_clarity_logo()
    create_overai_logo()
    create_overai_logo_bg()
