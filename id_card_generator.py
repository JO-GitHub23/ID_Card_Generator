from PIL import Image, ImageDraw, ImageFont
import os
import barcode
from barcode.writer import ImageWriter

def generate_id_card(company, name, phone, blood, address, id_no, photo_path, bg_path):
    # Paths setup
    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(base_dir, "fonts", "times.ttf")
    output_folder = os.path.join(base_dir, "static")

    # Open background image
    bg = Image.open(bg_path).convert("RGBA")
    bg = bg.resize((600, 900))  # standard card size

    draw = ImageDraw.Draw(bg)

    # Load fonts
    try:
        title_font = ImageFont.truetype(font_path, 45)
        label_font = ImageFont.truetype(font_path, 22)
        value_font = ImageFont.truetype(font_path, 26)
    except OSError:
        # fallback if font not found
        title_font = label_font = value_font = ImageFont.load_default()

    # Add company title
    draw.text((180, 50), f"{company} ID CARD", fill="black", font=title_font)

    # Add photo
    photo = Image.open(photo_path).resize((180, 180))
    bg.paste(photo, (210, 130))

    # Info layout start
    y = 350
    spacing = 80
    fields = [
        ("Name", name),
        ("Phone", phone),
        ("Blood Group", blood),
        ("Address", address),
        ("ID No", id_no),
    ]

    for label, value in fields:
        draw.text((70, y), f"{label}:", fill="black", font=label_font)
        draw.text((250, y), f"{value}", fill="black", font=value_font)
        y += spacing

    # Generate barcode for ID
    barcode_class = barcode.get_barcode_class('code128')
    my_barcode = barcode_class(str(id_no), writer=ImageWriter())
    barcode_path = os.path.join(output_folder, f"{id_no}_barcode.png")
    my_barcode.save(barcode_path)

    # Add barcode to card
    barcode_img = Image.open(f"{barcode_path}")
    barcode_img = barcode_img.resize((300, 100))
    bg.paste(barcode_img, (150, 750))

    # Save ID card
    output_file = os.path.join(output_folder, f"{name}_id_card.png")
    bg.save(output_file)

    return output_file
