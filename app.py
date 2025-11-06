from flask import Flask, render_template, request, send_file
import os
from id_card_generator import generate_id_card

# ✅ Explicitly define folders so Render can find them
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

@app.route('/')
def index():
    bg_path = os.path.join(STATIC_DIR, "backgrounds")
    bg_files = [f for f in os.listdir(bg_path) if f.endswith(".png")]
    return render_template("index.html", bg_list=bg_files)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        company = request.form['company']
        name = request.form['name']
        phone = request.form['phone']
        blood = request.form['blood']
        address = request.form['address']
        id_no = request.form['id_no']
        bg_choice = request.form['bg_choice']

        # Handle uploaded photo
        photo = request.files['photo']
        photo_path = os.path.join(STATIC_DIR, 'generated', photo.filename)
        photo.save(photo_path)

        bg_path = os.path.join(STATIC_DIR, "backgrounds", bg_choice)

        output_file = generate_id_card(
            company, name, phone, blood, address, id_no, photo_path, bg_path
        )

        return send_file(output_file, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
