from PIL import Image, ImageDraw, ImageFont
import ollama
from pathlib import Path
import textwrap
import os
import re
import random

def generate_caption(topic: str, style: str) -> str:
    prompt = f"Write a short, funny meme caption about '{topic}' in a {style} tone. Only respond with the caption — no bullet points or explanation."

    try:
        response = ollama.chat(
            model="gemma3n:e4b",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response["message"]["content"].strip()

        # Optionally split if the LLM still returns multiple options
        lines = re.split(r"\n\s*\n|\n\d+\.", content)
        caption_lines = [line.strip(" *•:-") for line in lines if len(line.strip()) > 0]
        return random.choice(caption_lines) if caption_lines else content
    except Exception as e:
        return f"[LLM error: {e}]"


def render_meme(image_path: Path, caption: str, output_dir="assets/output") -> Path:
    try:
        img = Image.open(image_path).convert("RGB")
    except Exception as e:
        raise RuntimeError(f"❌ Failed to load image: {e}")

    draw = ImageDraw.Draw(img)

    # Use a bigger font
    try:
        font = ImageFont.truetype("arial.ttf", size=40)
    except:
        font = ImageFont.load_default()

    # Wrap the caption to fit the image width
    wrapped = textwrap.wrap(caption, width=30)
    y_text = img.height - (len(wrapped) * 50) - 30  # bottom position

    for line in wrapped:
        bbox = font.getbbox(line)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        draw.text(
            ((img.width - w) / 2, y_text),
            line,
            font=font,
            fill="white",
            stroke_width=3,
            stroke_fill="black"
        )
        y_text += h + 10


    # Save output
    os.makedirs(output_dir, exist_ok=True)
    output_path = Path(output_dir) / f"meme_{image_path.stem}.png"
    img.save(output_path)
    return output_path
