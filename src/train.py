from tensorflow.keras import models, layers
import numpy as np

def train_model(X_train, y_train, X_test, y_test):
    num_classes = y_train.shape[1]  # fixes shape mismatch

    model = models.Sequential([
        layers.Conv2D(32, (3,3), activation="relu", input_shape=(224, 224, 1)),
        layers.MaxPooling2D((2,2)),

        layers.Conv2D(64, (3,3), activation="relu"),
        layers.MaxPooling2D((2,2)),

        layers.Conv2D(128, (3,3), activation="relu"),
        layers.MaxPooling2D((2,2)),

        layers.Flatten(),
        layers.Dense(128, activation="relu"),
        layers.Dense(num_classes, activation="softmax")  # ✅ fixed
    ])

    model.compile(optimizer="adam",
                  loss="categorical_crossentropy",
                  metrics=["accuracy"])

    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=10,
        batch_size=32
    )

    return model, history
