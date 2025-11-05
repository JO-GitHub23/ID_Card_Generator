from flask import Flask, render_template, request, send_from_directory
import os
from id_card_generator import generate_id_card

app = Flask(__name__)

# Folder setup
app.config["UPLOAD_FOLDER"] = os.path.join("static", "id_cards")
app.config["PHOTO_UPLOAD_FOLDER"] = os.path.join("static", "uploads")
app.config["BACKGROUND_FOLDER"] = os.path.join("static", "backgrounds")

# Create folders if missing
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["PHOTO_UPLOAD_FOLDER"], exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    company = request.form["company"]
    name = request.form["name"]
    phone = request.form["phone"]
    blood = request.form["blood"]
    address = request.form["address"]
    id_no = request.form["id_no"]
    bg_choice = request.form["bg_choice"]

    # Photo upload
    photo_file = request.files["photo"]
    photo_path = None
    if photo_file and photo_file.filename != "":
        photo_path = os.path.join(app.config["PHOTO_UPLOAD_FOLDER"], photo_file.filename)
        photo_file.save(photo_path)

    # Background selection
    if bg_choice == "custom":
        custom_bg = request.files["custom_bg"]
        if custom_bg and custom_bg.filename != "":
            bg_path = os.path.join(app.config["BACKGROUND_FOLDER"], custom_bg.filename)
            custom_bg.save(bg_path)
        else:
            bg_path = os.path.join(app.config["BACKGROUND_FOLDER"], "bg1.png")
    else:
        bg_path = os.path.join(app.config["BACKGROUND_FOLDER"], bg_choice)

    # Generate ID card
    output_file = generate_id_card(company, name, phone, blood, address, id_no, photo_path, bg_path)

    return render_template("index.html", generated=True, filename=os.path.basename(output_file))

@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)
    else:
        return f"❌ File not found: {filename}", 404

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

