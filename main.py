from pdf2image import convert_from_path
images = convert_from_path("aadhar.pdf",dpi=300,fmt='jpg')

for i, img in enumerate(images):
    img.save(f"page_{i+1}.jpg", "JPEG", quality=100)

