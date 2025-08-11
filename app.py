import os
import subprocess
from flask import Flask, request, send_file, render_template

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

app = Flask(__name__)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "pdf_file" not in request.files:
            return "No file uploaded", 400

        pdf_file = request.files["pdf_file"]
        if pdf_file.filename == "":
            return "No selected file", 400

        pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
        epub_path = os.path.join(OUTPUT_FOLDER, pdf_file.filename.rsplit(".", 1)[0] + ".epub")

        pdf_file.save(pdf_path)

        try:
            subprocess.run(["ebook-convert", pdf_path, epub_path], check=True)
        except subprocess.CalledProcessError:
            return "Conversion failed", 500

        return send_file(epub_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
