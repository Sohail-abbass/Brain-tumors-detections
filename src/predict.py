import numpy as np
import cv2
import joblib
from tensorflow.keras.models import load_model

# Load model + encoder
model = load_model("models/brain_tumor_cnn.h5")
encoder = joblib.load("models/label_encoder.pkl")
class_labels = list(encoder.classes_)

def predict_image(image_path: str):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (224, 224))
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=-1)  # channel dimension
    img = np.expand_dims(img, axis=0)   # batch dimension

    preds = model.predict(img)
    predicted_class = np.argmax(preds, axis=1)[0]
    confidence = np.max(preds)

    return class_labels[predicted_class], confidence


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=str, required=True, help="Path to MRI image")
    args = parser.parse_args()

    label, confidence = predict_image(args.image)
    print(f"🧠 Prediction: {label} (confidence: {confidence:.2f})")
