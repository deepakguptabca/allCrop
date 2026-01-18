from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image
from flask import Flask, send_file, request
from flask_cors import CORS
from io import BytesIO
import zipfile

app = Flask(__name__)

CORS(app)

@app.route("/test")
def test():
    return "server is running"

#for aadhar card
@app.route("/aadhar", methods=["POST"])
def aadhar():

    A4_WIDTH = 2480
    A4_HEIGHT = 3508
    y = 20

    a4_page = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")

    aadharPDF = request.files.getlist("File")

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

    img_buffer = BytesIO()
    a4_page.save(img_buffer, "JPEG", quality=100)
    img_buffer.seek(0)

    return send_file(img_buffer, mimetype="image/jpeg")

#for nsdl pan card
@app.route("/nsdlPan", methods=["POST"])
def nsdlPan():

    A4_WIDTH = 2480
    A4_HEIGHT = 3508
    y = 20

    a4_page = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")

    nsdlPanPDF = request.files.getlist("File")

    for pdf in nsdlPanPDF:
        images = convert_from_bytes(pdf.read(), dpi=300, fmt="jpg")

        for i, img in enumerate(images):

            # crop part
            left = 280
            top = 2700
            right = 2263
            bottom = 3329

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



#for uti pan card
@app.route("/utiPan", methods=["POST"])
def utiPan():

    A4_WIDTH = 2480
    A4_HEIGHT = 3508
    y = 20

    a4_page = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")

    utiPanPDF = request.files.getlist("File")

    for pdf in utiPanPDF:
        images = convert_from_bytes(pdf.read(), dpi=300, fmt="jpg")

        for i, img in enumerate(images):

            # crop part
            left = 147
            top = 2730
            right = 2335
            bottom = 3389

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

#for pvc aadhar card
@app.route("/pvcAadhar", methods=["POST"])
def pvcAadhar():

    pdf = request.files["File"]
    images = convert_from_bytes(pdf.read(), dpi=300, fmt="jpg")

    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:

        img = images[0]

        # ---------- FRONT ----------
        front = img.crop((200, 2385, 1260, 3060))
        front = front.resize((1017, 639))

        front_buffer = BytesIO()
        front.save(front_buffer, "JPEG", quality=100)

        zipf.writestr("aadhar_front.jpg", front_buffer.getvalue())

        # ---------- BACK ----------
        back = img.crop((1293, 2383, 2351,3063))  # adjust coords
        back = back.resize((1017, 639))

        back_buffer = BytesIO()
        back.save(back_buffer, "JPEG", quality=100)

        zipf.writestr("aadhar_back.jpg", back_buffer.getvalue())

    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        mimetype="application/zip",
        as_attachment=True,
        download_name="aadhar_pvc.zip"
    )


#for pawan qr prints
@app.route("/pawan", methods=["POST"])
def pawan():

    A4_WIDTH = 2480
    A4_HEIGHT = 3508
    y = 20
    x = 20

    a4_page = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")

    pawanPDF = request.files.getlist("File")

    for pdf in pawanPDF:
        images = convert_from_bytes(pdf.read(), dpi=300, fmt="jpg")

        for i, img in enumerate(images):

            resized = img.resize((943,1277))

            a4_page.paste(resized, (x, y))
            y += resized.height + 20

            if y + resized.height > A4_HEIGHT:
                break
            
    img_buffer = BytesIO()
    a4_page.save(img_buffer, "JPEG", quality=100)
    img_buffer.seek(0)

    return send_file(img_buffer, mimetype="image/jpeg")


if __name__ == "__main__":
    app.run(debug=True)