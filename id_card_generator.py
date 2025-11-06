from PIL import Image, ImageDraw, ImageFont
import os
import barcode
from barcode.writer import ImageWriter

def generate_id_card(company, name, phone, blood, address, id_no, photo_path, bg_path, output_dir):
    """
    Generate a portrait ID card PNG and return the full path.
    - bg_path: full path to background image (preset or uploaded)
    - photo_path: full path to user photo
    - output_dir: folder where generated images (barcode + final) are saved
    """

    # --- Load and prepare background (portrait) ---
    bg = Image.open(bg_path).convert("RGBA")
    # normalize to a consistent portrait size (width x height)
    CARD_W, CARD_H = 700, 1000
    bg = bg.resize((CARD_W, CARD_H))

    draw = ImageDraw.Draw(bg)

    # --- Fonts: Times New Roman bundled in static/fonts/times.ttf ---
    font_path = os.path.join("static", "fonts", "times.ttf")
    if not os.path.exists(font_path):
        # helpful error for debugging
        raise FileNotFoundError(f"Font not found: {font_path}. Please place times.ttf into static/fonts/")
    title_font = ImageFont.truetype(font_path, 46)
    label_font = ImageFont.truetype(font_path, 24)
    value_font = ImageFont.truetype(font_path, 28)

    # --- Company title (top center) ---
    draw.text((CARD_W//2, 50), company, font=title_font, fill="black", anchor="mm")

    # --- User photo (left of center near top) ---
    photo = Image.open(photo_path).convert("RGBA")
    PHOTO_W, PHOTO_H = 220, 280
    photo = photo.resize((PHOTO_W, PHOTO_H))
    photo_x = (CARD_W - PHOTO_W) // 2
    photo_y = 120
    bg.paste(photo, (photo_x, photo_y), photo)

    # --- Details area below photo ---
    y_start = photo_y + PHOTO_H + 30
    spacing = 60
    fields = [
        ("Name", name),
        ("Phone", phone),
        ("Blood", blood),
        ("Address", address),
        ("ID No", id_no)
    ]
    label_x = 70
    value_x = 300
    for i, (label, value) in enumerate(fields):
        y = y_start + i * spacing
        draw.text((label_x, y), f"{label}:", font=label_font, fill="black")
        # wrap long address if needed (simple)
        if label == "Address":
            # naive wrap: split into lines approx every 30 chars
            import textwrap
            lines = textwrap.wrap(str(value), width=30)
            for j, ln in enumerate(lines):
                draw.text((value_x, y + j*28), ln, font=value_font, fill="black")
            # adjust y_start shift if multi-line (not necessary for drawing final card)
        else:
            draw.text((value_x, y), str(value), font=value_font, fill="black")

    # --- Barcode generation (code128) ---
    barcode_class = barcode.get_barcode_class("code128")
    barcode_obj = barcode_class(str(id_no), writer=ImageWriter())

    barcode_base = os.path.join(output_dir, f"{id_no}_barcode")
    # barcode.save expects a base filename (without final .png in many cases)
    saved_path = barcode_obj.save(barcode_base)  # may return path with extension
    # ensure .png path
    if not saved_path.lower().endswith(".png"):
        saved_path = saved_path + ".png"

    # place barcode centered near bottom
    bar_img = Image.open(saved_path).convert("RGBA")
    BAR_W, BAR_H = 420, 110
    bar_img = bar_img.resize((BAR_W, BAR_H))
    bar_x = (CARD_W - BAR_W) // 2
    bar_y = CARD_H - BAR_H - 60
    bg.paste(bar_img, (bar_x, bar_y), bar_img)

    # --- Final save ---
    safe_name = f"{name.strip().replace(' ', '_')}_{id_no}.png"
    out_path = os.path.join(output_dir, safe_name)
    # convert to RGB to avoid transparency problems
    bg.convert("RGB").save(out_path, format="PNG")

    return out_path
