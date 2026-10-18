import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("SuperKart Sales Prediction")

# Section for online prediction
st.subheader("Online Prediction")


# Collect user input for property features
product_weight = st.number_input("Product Weight", min_value=1, value=10)
product_allocated_area = st.number_input("Product Allocated Area", min_value=0, value=2)
product_mrp = st.number_input("Product MRP", min_value=60, step=1, value=60)
store_establishment_year = st.number_input("Store Establishment Year", min_value=1900, step=50, value=1990)
product_sugar_content = st.selectbox("Sugar Content:", ["Low Sugar", "Regular", "No Sugar"])
product_type = st.selectbox("Product Type:", ["Baking Goods", "Canned", "Dairy", "Frozen Foods", "Household", "Health and Hygiene", "Snack Foods"])
store_size = st.selectbox("Store Size:", ["Small", "Medium", "High"])
store_location_city_type = st.selectbox("Store City Type:", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox("Store Type:", ["Departmental Store", "Supermarket Type1", "Supermarket Type2", "Food Mart"])

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'product_weight': product_weight,
    'product_allocated_area': product_allocated_area,
    'product_mrp': product_mrp,
    'store_establishment_year': store_establishment_year,
    'product_sugar_content': product_sugar_content,
    'product_type': product_type,
    'store_size': store_size,
    'store_location_city_type': store_location_city_type,
    'store_type': store_type
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/sales", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted Sales (in dollars)']
        st.success(f"Predicted Store Sales (in dollars): {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/salesbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")
