from flask import Flask, render_template, request, send_file
import os
from id_card_generator import generate_id_card

app = Flask(__name__, template_folder="templates", static_folder="static")

# Ensure required folders exist
os.makedirs(os.path.join("static", "generated"), exist_ok=True)
os.makedirs(os.path.join("static", "backgrounds"), exist_ok=True)
os.makedirs(os.path.join("static", "fonts"), exist_ok=True)

@app.route("/")
def index():
    bg_folder = os.path.join(app.root_path, "static", "backgrounds")
    bg_files = [f for f in os.listdir(bg_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    bg_files.sort()
    return render_template("index.html", bg_files=bg_files)

@app.route("/generate", methods=["POST"])
def generate():
    try:
        company = request.form["company"]
        name = request.form["name"]
        phone = request.form["phone"]
        blood = request.form["blood"]
        address = request.form["address"]
        id_no = request.form["id_no"]
        bg_name = request.form["bg_name"]

        # Save photo
        photo = request.files["photo"]
        photo_ext = os.path.splitext(photo.filename)[1]
        photo_path = os.path.join("static", "generated", f"{id_no}_photo{photo_ext}")
        photo.save(photo_path)

        bg_path = os.path.join("static", "backgrounds", bg_name)
        if not os.path.exists(bg_path):
            return f"Background '{bg_name}' not found.", 400

        # Generate ID Card
        output_file = generate_id_card(company, name, phone, blood, address, id_no, photo_path, bg_path)

        return send_file(output_file, as_attachment=True)

    except Exception as e:
        return f"Error: {e}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
