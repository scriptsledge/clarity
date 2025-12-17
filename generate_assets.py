from PIL import Image, ImageDraw, ImageFont
import os

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
    # Ensure assets dir exists
    assets_dir = os.path.join("frontend", "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    output_path = os.path.join(assets_dir, "logo.png")
    img.save(output_path, "PNG")
    print(f"Clarity Logo generated at {output_path}")

if __name__ == "__main__":
    create_clarity_logo()
