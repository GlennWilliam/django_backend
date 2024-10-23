import pickle
import os

def load_model():
    # Path to the model file
    model_path = 'django_backend/stocks/model.pkl'
    
    # Ensure the model file exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    
    # Load the model
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    # Check if the loaded object has a 'predict' method
    if not hasattr(model, 'predict'):
        raise AttributeError(f"Loaded object is not a valid model. Got: {type(model)}")
    
    return model

def predict_future_prices(historical_data, model, days=30):
    X = historical_data[['close_price']].values[-days:]  # Select the necessary columns
    
    # Make predictions for the next 'days'
    future_predictions = model.predict(X)
    
    print("Predictions:", future_predictions)  # Debugging print statement
    
    return future_predictions