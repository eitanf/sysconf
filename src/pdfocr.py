#!/usr/bin/python3
# This script converts a PDF file to text using the OCR method described in
# http://jonathansoma.com/lede/foundations-2017/classes/dealing-with-pdfs/commands-for-pdf-analysis/


import io
from PIL import Image
import pytesseract
import sys
from wand.image import Image as wi

if len(sys.argv) < 2:
    print("Requested arguments: PDF-file(s) to convert")
    sys.exit(-1)

for fn in sys.argv[1:]:
    basename = fn.split('.')[0]
    print("Processing", basename, "...")

    pdf = wi(filename = fn, resolution = 300)
    pdf_image = pdf.convert('jpeg')
    images = []
    out = open(basename + ".txt", "w")

    for img in pdf_image.sequence:
        ImgPage = wi(image = img)
        images.append(ImgPage.make_blob('jpeg'))

    for image in images:
        im = Image.open(io.BytesIO(image))
        text = pytesseract.image_to_string(im, lang='eng')
        out.write(text)

    out.close()

