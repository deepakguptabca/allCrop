from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image
from flask import Flask, render_template, send_file, request
from flask_cors import CORS
from io import BytesIO
import zipfile
import webbrowser
import threading
import os
import sys
import webbrowser

Image.MAX_IMAGE_PIXELS = 200_000_000


app = Flask(__name__)


CORS(app)

@app.route("/")
def home():
    return render_template("index.html")


#for aadhar card
@app.route("/aadhar", methods=["POST"])
def aadhar():

    A4_WIDTH = 2480
    A4_HEIGHT = 3508
    y = 60

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

            scale = 0.95  # 70% of original size

            new_width = int(cropped.width * scale)
            new_height = int(cropped.height * scale)

            cropped = cropped.resize((new_width, new_height), Image.LANCZOS)

            x = (A4_WIDTH - cropped.width) // 2
            a4_page.paste(cropped, (x, y))
            y += cropped.height + 20

            if y + cropped.height > A4_HEIGHT:
                break
            
    img_buffer = BytesIO()
    a4_page.save(img_buffer, "JPEG", quality=100)
    img_buffer.seek(0)

    return send_file(img_buffer, mimetype="image/jpeg",as_attachment=True,download_name="aadhar_cards.jpg")


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

    return send_file(img_buffer, mimetype="image/jpeg",as_attachment=True,download_name="pan_card.jpg")



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

    return send_file(img_buffer, mimetype="image/jpeg",as_attachment=True,download_name="pancard.jpg")


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



from flask import request, send_file, jsonify
from pdf2image import convert_from_bytes
from PIL import Image
from io import BytesIO

#voter card
@app.route("/voter", methods=["POST"])
def voter():

    # A4 output dimensions at 300 DPI
    A4_WIDTH = 2480
    A4_HEIGHT = 3508

    # Reference dimensions used when calculating crop coordinates
    REF_WIDTH = 2480
    REF_HEIGHT = 3508

    # Original crop coordinates
    REF_LEFT = 134
    REF_TOP = 393
    REF_RIGHT = 2386
    REF_BOTTOM = 1039

    # Output crop dimensions
    CROP_WIDTH = REF_RIGHT - REF_LEFT
    CROP_HEIGHT = REF_BOTTOM - REF_TOP

    GAP = 20
    y = 20

    # Create blank A4 page
    a4_page = Image.new(
        "RGB",
        (A4_WIDTH, A4_HEIGHT),
        "white"
    )

    voterPDF = request.files.getlist("File")

    if not voterPDF or all(not f.filename for f in voterPDF):
        return jsonify({"error": "Please upload a PDF file"}), 400

    try:

        for pdf in voterPDF:

            if not pdf.filename:
                continue

            # Convert PDF into images
            # 150 DPI reduces memory consumption
            images = convert_from_bytes(
                pdf.read(),
                dpi=150,
                fmt="jpeg"
            )

            for i, img in enumerate(images):

                print(f"Original PDF dimensions: {img.size}")

                # Calculate scaling factors
                scale_x = img.width / REF_WIDTH
                scale_y = img.height / REF_HEIGHT

                # Scale crop coordinates
                left = int(REF_LEFT * scale_x)
                top = int(REF_TOP * scale_y)

                right = int(REF_RIGHT * scale_x)
                bottom = int(REF_BOTTOM * scale_y)

                print(
                    f"Crop coordinates: "
                    f"{left}, {top}, {right}, {bottom}"
                )

                # Crop voter card
                cropped = img.crop((
                    left,
                    top,
                    right,
                    bottom
                ))

                # Resize to reference output dimensions
                cropped = cropped.resize(
                    (CROP_WIDTH, CROP_HEIGHT),
                    Image.Resampling.LANCZOS
                )

                print(f"Final crop dimensions: {cropped.size}")

                # Check available A4 space
                if y + cropped.height > A4_HEIGHT:
                    print("A4 page is full.")
                    break

                # Center horizontally
                x = (A4_WIDTH - cropped.width) // 2

                # Paste onto A4 page
                a4_page.paste(cropped, (x, y))

                # Update vertical position
                y += cropped.height + GAP

                img.close()

            # Stop if the page is full
            if y + CROP_HEIGHT > A4_HEIGHT:
                break

        # Generate output image
        img_buffer = BytesIO()

        a4_page.save(
            img_buffer,
            format="JPEG",
            quality=100
        )

        img_buffer.seek(0)

        return send_file(
            img_buffer,
            mimetype="image/jpeg",
            as_attachment=True,
            download_name="voter_card.jpg"
        )

    except Exception as e:

        print("Voter API Error:", str(e))

        return jsonify({
            "error": str(e)
        }), 500

    finally:
        a4_page.close()

def open_browser():
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()

    app.run(
        host="127.0.0.1",
        port=8000,
        debug=False
    )