from pdf2image import convert_from_path,convert_from_bytes
from PIL import Image
from flask import Flask,send_file,request
from io import BytesIO

app = Flask(__name__)

@app.route('/test')
def test():
    return "server is running"

@app.route('/aadhar',methods=['POST'])
def aadhar():

    aadharPDF = request.files['aadharFile']
    images = convert_from_bytes(aadharPDF.read(),dpi=300,fmt='jpg')

    for i, img in enumerate(images):

        #crop part
        left = 200
        top = 2384
        right = 2350
        bottom = 3060

        cropped = img.crop((left,top,right,bottom))

    img_buffer = BytesIO()
    cropped.save(img_buffer, "JPEG", quality=100)
    img_buffer.seek(0)

    return send_file(img_buffer, mimetype='image/jpeg')



if __name__ == '__main__':
    app.run(debug=True)



