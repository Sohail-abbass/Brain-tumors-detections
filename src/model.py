# src/model.py
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

def build_custom_cnn(input_shape=(224, 224, 1), num_classes=4):
    model = Sequential([
        # Conv Layer 1
        Conv2D(32, (3,3), activation='relu', input_shape=input_shape),
        MaxPooling2D(pool_size=(2,2)),

        # Conv Layer 2
        Conv2D(64, (3,3), activation='relu'),
        MaxPooling2D(pool_size=(2,2)),

        # Conv Layer 3
        Conv2D(128, (3,3), activation='relu'),
        MaxPooling2D(pool_size=(2,2)),

        # Flatten + Dense
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),  # prevent overfitting
        Dense(num_classes, activation='softmax')  # output layer
    ])
    return model
