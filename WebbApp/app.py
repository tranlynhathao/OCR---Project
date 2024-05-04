from flask import Flask, render_template, request
import os
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array, array_to_img
from tensorflow.keras.preprocessing.image import load_img
from deeplearning import OCR
import numpy as np

app = Flask(__name__)

BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH, '/Path/to/WebbApp/static/upload')


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        upload_file = request.files['image_name']
        filename = upload_file.filename
        path_save = os.path.join(UPLOAD_PATH, filename)
        upload_file.save(path_save)

        # Thay đổi kích thước ảnh trước khi truyền vào hàm nhận diện
        resized_image_path = os.path.join(UPLOAD_PATH, 'resized_' + filename)
        resize_image(path_save, resized_image_path, target_size=(224, 224))

        text = OCR(resized_image_path, filename)

        return render_template('/templates/index.html', upload=True, upload_image=filename, text=text)

    return render_template('/templates/index.html', upload=False)


def resize_image(input_path, output_path, target_size):
    image = load_img(input_path, target_size=target_size)
    image.save(output_path)


if __name__ == "__main__":
    app.run(debug=True)
