import os
import cv2
import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical

def preprocess_image(img_path, target_size=(224, 224)):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, target_size)
    img = img.astype("float32") / 255.0
    return img

def load_data(train_dir="DATASET/classification/Training", test_dir="DATASET/classification/Testing", target_size=(224, 224)):
    def load_dataset(data_dir):
        images, labels = [], []
        for cls in os.listdir(data_dir):
            cls_path = os.path.join(data_dir, cls)
            for img_name in os.listdir(cls_path):
                img_path = os.path.join(cls_path, img_name)
                img = preprocess_image(img_path, target_size)
                images.append(img)
                labels.append(cls)

        images = np.array(images)
        labels = np.array(labels)
        images = np.expand_dims(images, axis=-1)
        return images, labels

    # Load train/test
    X_train, y_train = load_dataset(train_dir)
    X_test, y_test = load_dataset(test_dir)

    # Encode labels
    encoder = LabelEncoder()
    y_train_enc = encoder.fit_transform(y_train)
    y_test_enc = encoder.transform(y_test)

    # One-hot encode
    y_train_cat = to_categorical(y_train_enc)
    y_test_cat = to_categorical(y_test_enc)

    return X_train, y_train_cat, X_test, y_test_cat, encoder
