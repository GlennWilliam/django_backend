import pickle
from sklearn.linear_model import LinearRegression
import numpy as np

# Create a simple dataset
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([1, 2, 3, 4, 5])

# Train a Linear Regression model
model = LinearRegression()
model.fit(X, y)

# Save the trained model to a .pkl file
model_path = ''
with open(model_path, 'wb') as f:
    pickle.dump(model, f)

print("Model saved successfully!")