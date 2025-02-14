from flask import Flask, request
from io import BytesIO
from services.process_details import runNewOcr
import cProfile
import threading

app = Flask(__name__)

# If you want to profile the code
# def profile_function(func, *args, **kwargs):
#     profiler = cProfile.Profile()
#     profiler.enable()  # Start profiling
#     result = func(*args, **kwargs)
#     profiler.disable()  # Stop profiling
#     profiler.print_stats()  # Print the profiling results
#     return result

@app.route('/')
def home():
    return "Hello, and Welcome to the OCR API!"

@app.route('/ocr/newAll', methods=['POST'])

def newOcr():
    image_file = request.files.get('image')
    image_bytes = image_file.read()
    with open("invoice.png", "wb") as f:
        f.write(image_bytes)
    
    return runNewOcr()


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=5000)
