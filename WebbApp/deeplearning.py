# import os
# import numpy as np
# import cv2
# import tensorflow as tf
# from tensorflow.keras.preprocessing.image import load_img, img_to_array
# import tensorflow as tf

# # Đường dẫn tới mô hình
# MODEL_PATH = "/Users/tranlynhathao/Desktop/Automatic-License-Plate-Detection/WebbApp/object_detection/"

# # Load mô hình
# try:
#     model = tf.keras.models.load_model(MODEL_PATH)
#     print("Model loaded successfully.")
# except Exception as e:
#     print(f"Error loading the model: {e}")

# def object_detection(path, filename, target_size=(224, 224), input_shape=(28, 28, 1)):
#     # Read image
#     image = cv2.imread(path)
    
#     # Check if the image is read successfully
#     if image is None:
#         print(f"Error reading image at path: {path}")
#         return None
    
#     # Convert to RGB format
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
#     # Resize image
#     try:
#         resized_image = cv2.resize(image, target_size)
#     except cv2.error as e:
#         print(f"Error resizing image: {e}")
#         return None
    
#     # Data preprocessing
#     # Convert into array and get the normalized output
#     image_arr = resized_image / 255.0
#     flattened_image = image_arr.reshape(1, *target_size, 3)  # Change this line
    
#     # Resize to match the expected input shape of the model
#     resized_flat_image = cv2.resize(flattened_image, (input_shape[0], input_shape[1]))

#     # Make predictions
#     coords = model.predict(resized_flat_image)
    
#     # Denormalize the values
#     h, w, _ = image_arr.shape
#     denorm = np.array([w, w, h, h])
#     coords = coords * denorm
#     coords = coords.astype(np.int32)

#     # Draw bounding box on top of the image
#     xmin, xmax, ymin, ymax = coords[0]
#     pt1 = (xmin, ymin)
#     pt2 = (xmax, ymax)
#     print(pt1, pt2)
#     cv2.rectangle(resized_image, pt1, pt2, (0, 255, 0), 3)

#     # Convert into BGR
#     image_bgr = cv2.cvtColor(resized_image, cv2.COLOR_RGB2BGR)
#     cv2.imwrite(
#         '/Users/tranlynhathao/Desktop/Automatic-License-Plate-Detection/WebbApp/static/predict/{}'.format(filename), image_bgr)
#     return coords




# def OCR(path, filename):
#     img = np.array(load_img(path))
#     cods = object_detection(path, filename)  # Thêm tham số filename
#     xmin, xmax, ymin, ymax = cods[0]
#     roi = img[ymin:ymax, xmin:xmax]
#     roi_bgr = cv2.cvtColor(roi, cv2.COLOR_RGB2BGR)
#     gray = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2GRAY)
#     magic_color = apply_brightness_contrast(gray, brightness=40, contrast=70)
#     cv2.imwrite(
#         '/Users/tranlynhathao/Desktop/Automatic-License-Plate-Detection/WebbApp/static/roi/{}'.format(filename), roi_bgr)

#     text = OCR(resized_image_path, filename, target_size=(224, 224))

#     print(text)
#     save_text(filename, text)
#     return text


# def apply_brightness_contrast(input_img, brightness=0, contrast=0):
#     if brightness != 0:
#         if brightness > 0:
#             shadow = brightness
#             highlight = 255
#         else:
#             shadow = 0
#             highlight = 255 + brightness
#         alpha_b = (highlight - shadow) / 255
#         gamma_b = shadow
#         buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
#     else:
#         buf = input_img.copy()

#     if contrast != 0:
#         f = 131 * (contrast + 127) / (127 * (131 - contrast))
#         alpha_c = f
#         gamma_c = 127 * (1 - f)
#         buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

#     return buf


import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import pytesseract as pt
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array, array_to_img
MODEL_PATH = "/Path/to/WebbApp/object_detection/"
model = tf.keras.models.load_model(MODEL_PATH)

try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading the model: {e}")

def object_detection(path, filename):
    # Read image
    target_size = (224, 224)  # Define the target size
    image = load_img(path)  # PIL object
    image = np.array(image, dtype=np.uint8)  # 8 bit array (0,255)
    image1 = load_img(path, target_size=target_size)
    # Data preprocessing
    image_arr = image / 255.0
    test_arr = image_arr.reshape(1, *target_size, 3)
    # Convert into array and get the normalized output
    image_arr_224 = img_to_array(image1)/255.0
    h, w, d = image.shape
    test_arr = image_arr_224.reshape(1, 224, 224, 3)
    # Make predictions
    coords = model.predict(test_arr)
    # Denormalize the values
    denorm = np.array([w, w, h, h])
    coords = coords * denorm
    coords = coords.astype(np.int32)
    # Draw bounding on top the image
    xmin, xmax, ymin, ymax = coords[0]
    pt1 = (xmin, ymin)
    pt2 = (xmax, ymax)
    print(pt1, pt2)
    cv2.rectangle(image, pt1, pt2, (0, 255, 0), 3)
    # Convert into bgr
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(
        '/Path/to/WebbApp/static/predict/{}'.format(filename), image_bgr)
    return coords


def save_text(filename, text):
    name, ext = os.path.splitext(filename)
    with open('/Path/to/WebbApp/static/predict/{}.txt'.format(name), mode='w') as f:
        f.write(text)
    f.close()


def OCR(image_path, filename):
    img = np.array(load_img(image_path))
    
    # Convert NumPy array to PIL Image
    pil_image = Image.fromarray(img)

    # Save the PIL Image to a temporary file
    temp_path = '/Path/to/WebbApp/static/upload/{}.jpeg'  # Provide an actual path
    pil_image.save(temp_path)

    cods = object_detection(temp_path, filename)
    xmin, xmax, ymin, ymax = cods[0]
    roi = img[ymin:ymax, xmin:xmax]
    roi_bgr = cv2.cvtColor(roi, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2GRAY)
    magic_color = apply_brightness_contrast(gray, brightness=40, contrast=70)
    cv2.imwrite(
        '/Path/to/WebbApp/static/roi/{}'.format(filename), roi_bgr)

    text = pt.image_to_string(magic_color, lang='eng', config='--psm 6')
    print(text)
    save_text(filename, text)
    return text


def apply_brightness_contrast(input_img, brightness=0, contrast=0):

    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow

        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()

    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)

        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf
