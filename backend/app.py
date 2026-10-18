# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
superkart_sales_predictor_api = Flask("SuperKart Sales Predictor")

# Load the trained machine learning model
model = joblib.load("superkart_sales_prediction_model_v1_0.joblib")

# Define a route for the home page (GET request)
@superkart_sales_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Sales Prediction API!"

# Define an endpoint for single store sales prediction (POST request)
@superkart_sales_predictor_api.post('/v1/sales')
def predict_store_sales():
    """
    This function handles POST requests to the '/v1/sales' endpoint.
    It expects a JSON payload containing store details and returns
    the predicted store sale as a JSON response.
    """
    # Get the JSON data from the request body
    store_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = { 
        'Product_Weight': store_data['Product_Weight'], 
        'Product_Allocated_Area': store_data['Product_Allocated_Area'], 
        'Product_MRP': store_data['Product_MRP'],	
        'Store_Establishment_Year': store_data['Store_Establishment_Year'], 
        'Product_Sugar_Content': store_data['Product_Sugar_Content'],	
        'Product_Type': store_data['Product_Type'],	
        'Store_Size': store_data['Store_Size'],	
        'Store_Location_City_Type': store_data['Store_Location_City_Type'],	
        'Store_Type': store_data['Store_Type']
    }


    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction (get log_price)
    predicted_log_sale = model.predict(input_data)[0]

    # Calculate actual sales
    predicted_sale = np.exp(predicted_log_sale)

    # Convert predicted_sale to Python float
    predicted_sale = round(float(predicted_sale), 2)
    # The conversion above is needed as we convert the model prediction (log sale) to actual sale using np.exp, which returns predictions as NumPy float32 values.
    # When we send this value directly within a JSON response, Flask's jsonify function encounters a datatype error

    # Return the actual sale
    return jsonify({'Predicted Sale (in dollars)': predicted_sale})


# Define an endpoint for batch prediction (POST request)
@superkart_sales_predictor_api.post('/v1/salesbatch')
def predict_store_sales_batch():
    """
    This function handles POST requests to the '/v1/salesbatch' endpoint.
    It expects a CSV file containing store details for multiple stores
    and returns the predicted store sales as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all properties in the DataFrame (get log_prices)
    predicted_log_sales = model.predict(input_data).tolist()

    # Calculate actual sales
    predicted_sales = [round(float(np.exp(log_sale)), 2) for log_sale in predicted_log_sales]

    # Create a dictionary of predictions with property IDs as keys
    store_ids = input_data['Store_Id'].tolist()  # Assuming 'Store_Id' is the store ID column
    output_dict = dict(zip(store_ids, predicted_sales))  # Use actual sales

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    superkart_sales_predictor_api.run(debug=True)
