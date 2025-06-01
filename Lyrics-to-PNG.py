import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Settings
IMG_WIDTH, IMG_HEIGHT = 1920, 1080
FONT_SIZE = 150
FONT_PATH = "Georgia-Bold-SKF.ttf"  # Use the new bold Georgia font in the program's folder
TITLE_FILENAME = "title.png"
OUTPUT_BASE = "output"
TEXT_COLOR = (249, 239, 213, 255)  # #F9EFD5
SHADOW_COLOR = (0, 0, 0, 128)      # #000000, opacity 0.5
STROKE_COLOR = (0, 0, 0, 0)  # Fully transparent, just for clarity
STROKE_WIDTH = 0  # Remove stroke
SHADOW_OFFSET = (5, 5)
SHADOW_BLUR = 10
BG_COLOR = (77, 106, 95, 255)  # #4d6a5f
DOUBLE_SPACING = FONT_SIZE  # 150px for double-spacing
LINE_SPACING = FONT_SIZE // 2  # 75px for half-spacing between lines
KERNING = 5  # Increase kerning between letters by 5

def get_font():
    return ImageFont.truetype(FONT_PATH, FONT_SIZE)

def clear_or_create_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

def draw_text_with_effects(draw, text, font, position):
    # Shadow
    shadow_layer = Image.new("RGBA", (IMG_WIDTH, IMG_HEIGHT), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_layer)
    shadow_pos = (position[0] + SHADOW_OFFSET[0], position[1] + SHADOW_OFFSET[1])
    # Draw shadow with kerning
    _draw_text_with_kerning(shadow_draw, shadow_pos, text, font, SHADOW_COLOR)

    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=SHADOW_BLUR))

    # Smooth bevel: multiple highlight and shadow layers for a curved effect
    bevel_layer = Image.new("RGBA", (IMG_WIDTH, IMG_HEIGHT), (0, 0, 0, 0))
    bevel_draw = ImageDraw.Draw(bevel_layer)
    for offset, alpha in [((-4, -4), 40), ((-3, -3), 60), ((-2, -2), 80), ((-1, -1), 100)]:
        _draw_text_with_kerning(bevel_draw, (position[0] + offset[0], position[1] + offset[1]), text, font, (255,255,255,alpha))
    for offset, alpha in [((4, 4), 40), ((3, 3), 60), ((2, 2), 80), ((1, 1), 100)]:
        _draw_text_with_kerning(bevel_draw, (position[0] + offset[0], position[1] + offset[1]), text, font, (0,0,0,alpha))

    # Main text (no stroke)
    text_layer = Image.new("RGBA", (IMG_WIDTH, IMG_HEIGHT), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_layer)
    _draw_text_with_kerning(text_draw, position, text, font, TEXT_COLOR)

    # Composite layers
    base = Image.new("RGBA", (IMG_WIDTH, IMG_HEIGHT), (0, 0, 0, 0))
    base = Image.alpha_composite(base, shadow_layer)
    base = Image.alpha_composite(base, bevel_layer)
    base = Image.alpha_composite(base, text_layer)
    return base

def _draw_text_with_kerning(draw, position, text, font, fill):
    x, y = position
    for char in text:
        if char == '\n':
            y += font.size + LINE_SPACING
            x = position[0]
            continue
        draw.text((x, y), char, font=font, fill=fill)
        w = font.getlength(char) if hasattr(font, "getlength") else font.getsize(char)[0]
        x += w + KERNING

def center_text(draw, text, font):
    # Get bounding box: (left, top, right, bottom)
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=STROKE_WIDTH)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (IMG_WIDTH - w) // 2
    y = (IMG_HEIGHT - h) // 2
    return (x, y)

def main():
    # Read lyrics and split into blocks separated by blank lines
    with open("Lyrics.txt", "r", encoding="utf-8") as f:
        content = f.read()
    blocks = [block.strip().splitlines() for block in content.split('\n\n') if block.strip()]
    if not blocks:
        print("Lyrics.txt is empty.")
        return

    # Title image: all lines in the first block
    title_lines = [line.strip() for line in blocks[0] if line.strip()]
    output_folder = os.path.join(OUTPUT_BASE, title_lines[0])
    clear_or_create_folder(output_folder)
    font = get_font()

    # Draw title image (multi-line, centered horizontally per line, half-spacing)
    img = Image.new("RGBA", (IMG_WIDTH, IMG_HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    line_heights = []
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=font, stroke_width=STROKE_WIDTH)
        line_heights.append(bbox[3] - bbox[1])
    total_height = sum(line_heights) + (len(title_lines) - 1) * LINE_SPACING
    y = (IMG_HEIGHT - total_height) // 2
    for i, line in enumerate(title_lines):
        bbox = draw.textbbox((0, 0), line, font=font, stroke_width=STROKE_WIDTH)
        w = bbox[2] - bbox[0]
        x = (IMG_WIDTH - w) // 2
        img = Image.alpha_composite(img, draw_text_with_effects(draw, line, font, (x, y)))
        y += line_heights[i] + LINE_SPACING
    img.save(os.path.join(output_folder, TITLE_FILENAME))

    # Lyric images (each block after the first)
    for idx, block in enumerate(blocks[1:], 1):
        img = Image.new("RGBA", (IMG_WIDTH, IMG_HEIGHT), BG_COLOR)
        draw = ImageDraw.Draw(img)
        lines = [line.strip() for line in block if line.strip()]
        line_heights = []
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font, stroke_width=STROKE_WIDTH)
            line_heights.append(bbox[3] - bbox[1])
        total_height = sum(line_heights) + (len(lines) - 1) * LINE_SPACING
        y = (IMG_HEIGHT - total_height) // 2
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font, stroke_width=STROKE_WIDTH)
            w = bbox[2] - bbox[0]
            x = (IMG_WIDTH - w) // 2
            img = Image.alpha_composite(img, draw_text_with_effects(draw, line, font, (x, y)))
            y += line_heights[i] + LINE_SPACING
        filename = f"{idx:02d}.png"
        img.save(os.path.join(output_folder, filename))

if __name__ == "__main__":
    main()