# 🧠 Brain Tumor Detection Using MRI Scans

An AI-powered web application that detects and classifies brain tumors from MRI images using a Convolutional Neural Network (CNN).

> ⚠️ This project is built for educational and research purposes only. It is NOT a substitute for professional medical diagnosis.

---

## 🚀 Project Overview

This application allows users to upload a brain MRI image, and the trained deep learning model analyzes the scan to detect and classify the tumor type.

The system:
- Accepts MRI image input (JPG, JPEG, PNG)
- Validates whether the image resembles a brain MRI
- Preprocesses the image
- Uses a trained CNN model for classification
- Displays prediction results with confidence score

---

## 🧠 Tumor Classes

The model is trained to classify MRI scans into the following categories:

- 🟢 **No Tumor**
- 🔴 **Glioma**
- 🟡 **Meningioma**
- 🟠 **Pituitary Tumor**

---

## 🏗️ Tech Stack

### 🔹 Machine Learning
- Python
- TensorFlow / Keras
- OpenCV
- NumPy
- Joblib

### 🔹 Web Interface
- Streamlit

### 🔹 Version Control
- Git & GitHub

---

## ⚙️ How It Works

### 1️⃣ Image Upload
User uploads a brain MRI scan through the web interface.

### 2️⃣ MRI Validation
The system checks:
- Image dimensions
- Intensity distribution
- Edge density
- MRI-like characteristics

### 3️⃣ Preprocessing
- Convert to grayscale
- Resize to 224x224
- Normalize pixel values
- Expand dimensions for model input

### 4️⃣ Prediction
The trained CNN model:
- Predicts tumor class
- Calculates confidence score
- Displays probabilities for all classes

---

## 📊 Model Details

- Architecture: Convolutional Neural Network (CNN)
- Input Size: 224 x 224 (Grayscale)
- Output: Multi-class classification
- Loss Function: Categorical Crossentropy
- Optimizer: Adam

---
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate  # Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Run the App
streamlit run models/streamlit.py
