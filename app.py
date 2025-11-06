from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from id_card_generator import generate_id_card

app = Flask(__name__)

# Folders
ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(ROOT, "static")
BG_FOLDER = os.path.join(STATIC, "backgrounds")
GEN_FOLDER = os.path.join(STATIC, "generated")
FONT_FOLDER = os.path.join(STATIC, "fonts")

# Ensure folders exist
os.makedirs(BG_FOLDER, exist_ok=True)
os.makedirs(GEN_FOLDER, exist_ok=True)
os.makedirs(FONT_FOLDER, exist_ok=True)

ALLOWED_IMG = {".png", ".jpg", ".jpeg", ".webp"}

def allowed_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_IMG

@app.route("/")
def index():
    bg_files = sorted([f for f in os.listdir(BG_FOLDER) if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))])
    return render_template("index.html", bg_files=bg_files, preview_file=None)

@app.route("/generate", methods=["POST"])
def generate():
    try:
        # form fields
        company = request.form.get("company", "").strip()
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        blood = request.form.get("blood", "").strip()
        address = request.form.get("address", "").strip()
        id_no = request.form.get("id_no", "").strip()
        selected_bg = request.form.get("bg_name", "")

        # validate required
        if not (company and name and id_no):
            return "Company, Name and ID are required", 400

        # photo upload
        photo = request.files.get("photo")
        if not photo or photo.filename == "":
            return "Please upload a photo", 400
        if not allowed_file(photo.filename):
            return "Photo file type not allowed", 400

        photo_filename = secure_filename(f"{id_no}_photo{os.path.splitext(photo.filename)[1]}")
        photo_path = os.path.join(GEN_FOLDER, photo_filename)
        photo.save(photo_path)

        # custom background upload (preferred if present)
        custom_bg = request.files.get("custom_bg")
        bg_path = None
        if custom_bg and custom_bg.filename != "":
            if not allowed_file(custom_bg.filename):
                return "Background file type not allowed", 400
            custom_fname = secure_filename(f"{id_no}_bg{os.path.splitext(custom_bg.filename)[1]}")
            bg_path = os.path.join(GEN_FOLDER, custom_fname)
            custom_bg.save(bg_path)
        else:
            # use selected preset
            if not selected_bg:
                return "No background selected", 400
            preset_path = os.path.join(BG_FOLDER, secure_filename(selected_bg))
            if not os.path.exists(preset_path):
                return f"Preset background not found: {selected_bg}", 400
            bg_path = preset_path

        # Generate ID card (returns full path)
        output_path = generate_id_card(
            company=company,
            name=name,
            phone=phone,
            blood=blood,
            address=address,
            id_no=id_no,
            photo_path=photo_path,
            bg_path=bg_path,
            output_dir=GEN_FOLDER
        )

        # For preview on same page, we pass relative path under static/
        preview_rel = os.path.relpath(output_path, STATIC).replace("\\", "/")  # e.g. generated/name_id_card.png

        # list backgrounds again for template
        bg_files = sorted([f for f in os.listdir(BG_FOLDER) if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))])

        return render_template("index.html", bg_files=bg_files, preview_file=preview_rel, download_name=os.path.basename(output_path))

    except Exception as e:
        # debug info while developing — in production you'd hide this
        return render_template("error.html", error=str(e)), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
