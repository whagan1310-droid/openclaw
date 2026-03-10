from PIL import Image, ImageEnhance
import os

# S.A.M.P.I.RT Visual Forge: Multi-Color Siren Generator
# This script creates animated pulsing GIFs in Red, Yellow, Green, and Blue.

def create_pulsing_gif(base_image_path, color_name, output_dir="assets/sirens"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    img = Image.open(base_image_path).convert("RGBA")
    frames = []
    
    # Create a 10-frame pulse effect (Dim -> Bright -> Dim)
    # Frame sequence: 0.5x brightness up to 1.5x and back
    factors = [0.6, 0.8, 1.0, 1.2, 1.4, 1.5, 1.4, 1.2, 1.0, 0.8]
    
    for factor in factors:
        enhancer = ImageEnhance.Brightness(img)
        frame = enhancer.enhance(factor)
        frames.append(frame)
    
    output_path = f"{output_dir}/{color_name}_siren.gif"
    frames[0].save(
        output_path, 
        save_all=True, 
        append_images=frames[1:], 
        duration=80, 
        loop=0
    )
    print(f"✅ Generated {color_name} siren at {output_path}")

if __name__ == "__main__":
    # Paths to generated base images (placeholders for absolute paths)
    # Note: Antigravity will populate these with real paths during execution
    bases = {
        "amber": "C:/Users/Gam3rGoon/.gemini/antigravity/brain/ca3765c1-6c78-49c2-8799-98341b7a9fb1/siren_base_amber_1773115948896.png",
        "green": "C:/Users/Gam3rGoon/.gemini/antigravity/brain/ca3765c1-6c78-49c2-8799-98341b7a9fb1/siren_base_green_1773115962300.png",
        "blue": "C:/Users/Gam3rGoon/.gemini/antigravity/brain/ca3765c1-6c78-49c2-8799-98341b7a9fb1/siren_base_blue_1773115974238.png",
        "red": "C:/Users/Gam3rGoon/.gemini/antigravity/brain/ca3765c1-6c78-49c2-8799-98341b7a9fb1/siren_base_red_1773116040440.png"
    }
    
    for color, path in bases.items():
        if os.path.exists(path):
            create_pulsing_gif(path, color)
        else:
            print(f"⚠️ Skipping {color}: Base not found at {path}")
