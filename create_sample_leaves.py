"""
Utility script to generate realistic sample plant leaf images
with realistic textures, veins, and disease lesions (healthy, early blight, powdery mildew, common rust).
"""

import os
import math
from PIL import Image, ImageDraw, ImageFilter

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "sample_images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def draw_base_leaf(width=500, height=600, leaf_color=(34, 139, 34)):
    """Draw a realistic leaf silhouette with main vein and lateral veins."""
    img = Image.new("RGBA", (width, height), (245, 247, 245, 255))
    draw = ImageDraw.Draw(img)

    # Leaf center and axis
    cx, cy = width // 2, height // 2
    
    # Draw leaf blade shape using polygon
    points = []
    # Tip at top
    points.append((cx, 60))
    # Right side lobe
    for y in range(80, 520, 20):
        t = (y - 80) / 440.0
        # Oval curve width
        w = math.sin(t * math.pi) * 160 + math.sin(t * math.pi * 3) * 15
        points.append((cx + w, y))
    # Petiole bottom
    points.append((cx + 10, 540))
    points.append((cx - 10, 540))
    # Left side lobe
    for y in range(500, 60, -20):
        t = (y - 80) / 440.0
        w = math.sin(t * math.pi) * 160 + math.sin(t * math.pi * 3) * 15
        points.append((cx - w, y))

    draw.polygon(points, fill=leaf_color, outline=(25, 100, 25))

    # Leaf blade texture / shading
    inner_mask = Image.new("L", (width, height), 0)
    inner_draw = ImageDraw.Draw(inner_mask)
    inner_draw.polygon(points, fill=255)

    # Main vein (midrib)
    draw.line([(cx, 60), (cx, 540)], fill=(70, 160, 60), width=6)
    
    # Lateral secondary veins
    for y in range(120, 480, 40):
        t = (y - 80) / 440.0
        w = math.sin(t * math.pi) * 130
        draw.line([(cx, y), (cx + w, y - 25)], fill=(60, 150, 55), width=3)
        draw.line([(cx, y), (cx - w, y - 25)], fill=(60, 150, 55), width=3)

    return img.convert("RGB")


def create_healthy_leaf():
    img = draw_base_leaf(leaf_color=(45, 155, 45))
    path = os.path.join(OUTPUT_DIR, "healthy_tomato_leaf.jpg")
    img.save(path, "JPEG", quality=95)
    return path


def create_early_blight_leaf():
    img = draw_base_leaf(leaf_color=(50, 140, 45))
    draw = ImageDraw.Draw(img)

    # Concentric brown rings (target board pattern)
    lesions = [
        (220, 240, 45),
        (310, 320, 38),
        (180, 380, 52),
        (280, 180, 32)
    ]

    for lx, ly, radius in lesions:
        # Yellow chlorotic halo
        draw.ellipse([lx - radius - 15, ly - radius - 15, lx + radius + 15, ly + radius + 15], fill=(210, 200, 40))
        # Brown outer ring
        draw.ellipse([lx - radius, ly - radius, lx + radius, ly + radius], fill=(90, 50, 20))
        # Inner tan ring
        draw.ellipse([lx - radius + 8, ly - radius + 8, lx + radius - 8, ly + radius - 8], fill=(135, 80, 35))
        # Dark brown concentric ring
        draw.ellipse([lx - radius + 16, ly - radius + 16, lx + radius - 16, ly + radius - 16], fill=(70, 35, 15))
        # Center core
        draw.ellipse([lx - 5, ly - 5, lx + 5, ly + 5], fill=(40, 20, 10))

    img = img.filter(ImageFilter.GaussianBlur(radius=0.7))
    path = os.path.join(OUTPUT_DIR, "early_blight_leaf.jpg")
    img.save(path, "JPEG", quality=95)
    return path


def create_powdery_mildew_leaf():
    img = draw_base_leaf(leaf_color=(40, 130, 40))
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Fluffy white/ash patches
    mildew_spots = [
        (250, 200, 60),
        (190, 290, 75),
        (320, 330, 70),
        (240, 410, 80),
        (290, 140, 45)
    ]

    for sx, sy, r in mildew_spots:
        for i in range(12):
            ox = sx + math.sin(i * 1.5) * (r * 0.5)
            oy = sy + math.cos(i * 1.5) * (r * 0.5)
            draw.ellipse([ox - r * 0.6, oy - r * 0.6, ox + r * 0.6, oy + r * 0.6], fill=(240, 242, 240, 160))

    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=4))
    img.paste(overlay, (0, 0), overlay)
    
    path = os.path.join(OUTPUT_DIR, "powdery_mildew_leaf.jpg")
    img.save(path, "JPEG", quality=95)
    return path


def create_common_rust_leaf():
    img = draw_base_leaf(leaf_color=(45, 140, 45))
    draw = ImageDraw.Draw(img)

    # Cinnamon-orange raised rust pustules
    rust_centers = [
        (200, 200), (220, 210), (250, 190), (270, 240),
        (180, 290), (210, 310), (230, 280), (310, 290),
        (190, 370), (220, 390), (260, 360), (300, 380),
        (240, 440), (270, 430), (200, 450), (290, 210)
    ]

    for rx, ry in rust_centers:
        # Yellowish fleck halo
        draw.ellipse([rx - 12, ry - 12, rx + 12, ry + 12], fill=(225, 205, 50))
        # Orange rust pustule
        draw.ellipse([rx - 7, ry - 7, rx + 7, ry + 7], fill=(210, 95, 20))
        # Dark brown center
        draw.ellipse([rx - 3, ry - 3, rx + 3, ry + 3], fill=(120, 45, 15))

    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    path = os.path.join(OUTPUT_DIR, "common_rust_leaf.jpg")
    img.save(path, "JPEG", quality=95)
    return path


if __name__ == "__main__":
    p1 = create_healthy_leaf()
    p2 = create_early_blight_leaf()
    p3 = create_powdery_mildew_leaf()
    p4 = create_common_rust_leaf()
    print("Created sample leaves:", [p1, p2, p3, p4])
