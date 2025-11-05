from PIL import Image, ImageDraw, ImageFont
import os
import barcode
from barcode.writer import ImageWriter

def generate_id_card(company, name, phone, blood, address, id_no, photo_path, bg_path):
    # Card size (portrait)
    width, height = 600, 900

    # Load background
    bg = Image.open(bg_path).convert("RGBA")
    bg = bg.resize((width, height))

    draw = ImageDraw.Draw(bg)

    # Fonts
    title_font = ImageFont.truetype("arialbd.ttf", 40)
    label_font = ImageFont.truetype("arial.ttf", 22)
    value_font = ImageFont.truetype("arialbd.ttf", 24)

    # Company Name
    draw.text((width / 2 - len(company) * 8, 40), company, fill="white", font=title_font)

    # Photo
    if photo_path:
        photo = Image.open(photo_path).convert("RGBA")
        photo = photo.resize((180, 180))
        bg.paste(photo, (width // 2 - 90, 110))

    # Fields start position
    y_start = 320
    spacing = 80

    # Labels and Values
    details = [
        ("Name", name),
        ("Phone", phone),
        ("Blood Group", blood),
        ("Address", address),
        ("ID No", id_no)
    ]

    for i, (label, value) in enumerate(details):
        y = y_start + i * spacing
        draw.text((70, y), f"{label}:", fill="black", font=label_font)
        draw.text((250, y), value, fill="black", font=value_font)

    # Barcode generation
    barcode_path = os.path.join("static", "id_cards", f"{id_no}_barcode.png")
    code128 = barcode.get('code128', id_no, writer=ImageWriter())
    code128.save(barcode_path[:-4])

    # Paste barcode at bottom
    bar_img = Image.open(barcode_path).resize((400, 100))
    bg.paste(bar_img, (width // 2 - 200, height - 150))

    # Save final image
    output_folder = os.path.join("static", "id_cards")
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f"{id_no}_idcard.png")
    bg.save(output_path)

    return output_path
