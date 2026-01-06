from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image
from flask import Flask, send_file, request
from io import BytesIO

app = Flask(__name__)

@app.route("/test")
def test():
    return "server is running"


@app.route("/aadhar", methods=["POST"])
def aadhar():

    A4_WIDTH = 2480
    A4_HEIGHT = 3508
    y = 20

    a4_page = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")

    aadharPDF = request.files.getlist("aadharFile")

    for pdf in aadharPDF:
        images = convert_from_bytes(pdf.read(), dpi=300, fmt="jpg")

        for i, img in enumerate(images):

            # crop part
            left = 200
            top = 2384
            right = 2350
            bottom = 3060

            cropped = img.crop((left, top, right, bottom))

            x = (A4_WIDTH - cropped.width) // 2
            a4_page.paste(cropped, (x, y))
            y += cropped.height + 20

            if y + cropped.height > A4_HEIGHT:
                break

    img_buffer = BytesIO()
    a4_page.save(img_buffer, "JPEG", quality=100)
    img_buffer.seek(0)

    return send_file(img_buffer, mimetype="image/jpeg")


if __name__ == "__main__":
    app.run(debug=True)
