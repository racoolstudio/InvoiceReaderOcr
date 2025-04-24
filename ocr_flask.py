from flask import Flask, request, jsonify
from io import BytesIO
from services.process_details import getInfo
from services.table import get_table
from services.detect_vendor import getVendorName
from PIL import Image
app = Flask(__name__)


@app.route('/')
def home():
    return "Hello, and Welcome to the OCR API!"

@app.route('/ocr/getAll', methods=['POST'])
def getAll():
    image_file = request.files.get('image')
    image_bytes = image_file.read()
    with open("invoice.png", "wb") as f:
        f.write(image_bytes)
    
    info=getInfo()
    table=get_table()

    return jsonify(info,table)


# Uncomment if you are deploying it locally and not using docker 
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)