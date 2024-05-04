model_path = "/Path/to/WebbApp/object_detection/saved_model.pbtxt"

try:
    model = tf.keras.models.load_model(model_path)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading the model: {e}")
