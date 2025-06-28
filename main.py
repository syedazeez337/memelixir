from meme_utils import generate_caption, render_meme
from pathlib import Path

# === Basic configuration ===
image_path = Path("assets/distracted_boyfriend.jpg")
style = "genz"
topic = "job hunting"

# === Run MemeForge ===
print(f"🎯 Generating meme for topic: '{topic}' in style: '{style}'...")
caption = generate_caption(topic, style)
print(f"💬 Caption generated: {caption}")

output_path = render_meme(image_path, caption)
print(f"✅ Meme saved to: {output_path}")
