from PIL import Image, ImageDraw, ImageFont
import os
import barcode
from barcode.writer import ImageWriter

def generate_id_card(company, name, phone, blood, address, id_no, photo_path, bg_path):
    # Load background (portrait)
    bg = Image.open(bg_path).convert("RGBA")
    bg = bg.resize((700, 1000))

    draw = ImageDraw.Draw(bg)

    # Load font
    font_path = os.path.join("static", "fonts", "times.ttf")
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font not found: {font_path}")

    title_font = ImageFont.truetype(font_path, 45)
    label_font = ImageFont.truetype(font_path, 28)
    value_font = ImageFont.truetype(font_path, 30)

    # Company name (top center)
    draw.text((bg.width // 2, 40), company, font=title_font, fill="black", anchor="mm")

    # Employee photo
    photo = Image.open(photo_path).resize((200, 250))
    bg.paste(photo, (250, 100))

    # Info positions
    y_start = 380
    spacing = 60

    fields = [
        ("Name", name),
        ("Phone", phone),
        ("Blood Group", blood),
        ("Address", address),
        ("ID No", id_no)
    ]

    for label, value in fields:
        draw.text((80, y_start), f"{label}:", fill="black", font=label_font)
        draw.text((300, y_start), value, fill="black", font=value_font)
        y_start += spacing

    # Generate barcode
    barcode_filename = os.path.join("static", "generated", f"{id_no}_barcode")
    CODE128 = barcode.get_barcode_class('code128')
    my_code = CODE128(id_no, writer=ImageWriter())
    barcode_path = my_code.save(barcode_filename)

    # Fix double .png
    if not barcode_path.endswith(".png"):
        barcode_path = barcode_path + ".png"

    barcode_img = Image.open(barcode_path).resize((400, 100))
    bg.paste(barcode_img, (150, y_start + 20))

    # Output
    output_path = os.path.join("static", "generated", f"{name.replace(' ', '_')}_id_card.png")
    bg.save(output_path)

    return output_path
