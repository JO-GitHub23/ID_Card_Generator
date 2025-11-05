from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
import os

def generate_id_card(company, name, phone, blood, address, id_no, photo_path, bg_path):
    # Load the background image
    bg = Image.open(bg_path).convert("RGB")
    bg = bg.resize((600, 900))  # portrait size

    draw = ImageDraw.Draw(bg)

    # ---- FONT SETUP ----
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 40)
        label_font = ImageFont.truetype("arial.ttf", 26)
        value_font = ImageFont.truetype("arial.ttf", 28)
    except OSError:
        title_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        value_font = ImageFont.load_default()

    # ---- TITLE ----
    draw.text((150, 30), f"{company} ID CARD", fill="black", font=title_font)

    # ---- PHOTO ----
    if photo_path and os.path.exists(photo_path):
        photo = Image.open(photo_path).convert("RGB")
        photo = photo.resize((180, 180))
        bg.paste(photo, (210, 100))  # center top

    # ---- DETAILS ----
    y_start = 320
    line_gap = 60
    details = [
        ("Name", name),
        ("Phone", phone),
        ("Blood Group", blood),
        ("Address", address),
        ("ID No", id_no),
    ]

    for i, (label, value) in enumerate(details):
        y = y_start + i * line_gap
        draw.text((70, y), f"{label}:", fill="black", font=label_font)
        draw.text((250, y), str(value), fill="black", font=value_font)

    # ---- BARCODE ----
    barcode_path = f"static/id_cards/{id_no}_barcode.png"
    EAN = barcode.get_barcode_class("code128")
    ean = EAN(str(id_no), writer=ImageWriter())
    ean.save(barcode_path.replace(".png", ""))

    barcode_img = Image.open(barcode_path)
    barcode_img = barcode_img.resize((350, 100))
    bg.paste(barcode_img, (125, 750))  # bottom center

    # ---- SAVE FINAL CARD ----
    output_file = f"static/id_cards/{name}_id_card.png"
    bg.save(output_file)

    return output_file
