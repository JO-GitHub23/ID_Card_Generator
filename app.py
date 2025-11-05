from flask import Flask, render_template, request, send_file
import os
from id_card_generator import generate_id_card

app = Flask(__name__)

# Folder setup
os.makedirs("static/id_cards", exist_ok=True)
os.makedirs("static/backgrounds", exist_ok=True)

@app.route("/")
def index():
    # get available background images
    bg_list = os.listdir("static/backgrounds")
    return render_template("index.html", bg_list=bg_list)

@app.route("/generate", methods=["POST"])
def generate():
    try:
        company = request.form["company"]
        name = request.form["name"]
        phone = request.form["phone"]
        blood = request.form["blood"]
        address = request.form["address"]
        id_no = request.form["id_no"]
        bg_choice = request.form["bg_choice"]

        bg_path = os.path.join("static/backgrounds", bg_choice)

        # photo upload
        photo = request.files["photo"]
        photo_path = None
        if photo:
            photo_path = os.path.join("static/id_cards", photo.filename)
            photo.save(photo_path)

        output_file = generate_id_card(company, name, phone, blood, address, id_no, photo_path, bg_path)
        return send_file(output_file, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)