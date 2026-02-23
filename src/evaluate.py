# src/evaluate.py

def evaluate_model(model, X_test, y_test):
    """Evaluate the trained model on test data and print results."""
    loss, accuracy = model.evaluate(X_test, y_test, verbose=1)
    print(f"📊 Test Loss: {loss:.4f}")
    print(f"📈 Test Accuracy: {accuracy:.4f}")
    return loss, accuracy
