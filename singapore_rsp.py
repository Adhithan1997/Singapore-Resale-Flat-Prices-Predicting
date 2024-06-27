import streamlit as st
import numpy as np
import pickle

# Load the model
with open('dt.pkl', 'rb') as f:
    model = pickle.load(f)

# Load encoders
with open('town_encoder.pkl', 'rb') as f:
    town_encoder = pickle.load(f)
with open('flat_type_encoder.pkl', 'rb') as f:
    flat_type_encoder = pickle.load(f)
with open('storey_range_encoder.pkl', 'rb') as f:
    storey_range_encoder = pickle.load(f)
with open('flat_model_encoder.pkl', 'rb') as f:
    flat_model_encoder = pickle.load(f)
with open('street_name_encoder.pkl', 'rb') as f:
    street_name_encoder = pickle.load(f)

# Streamlit code
st.set_page_config(layout="wide")
st.write("""
<div style='text-align:center'>
    <h1 style='color:#1E90FF;'>Singapore Resale Flat Price Prediction Application</h1>
</div>
""", unsafe_allow_html=True)

st.title(":red[Resale Price Prediction]")
features_list = ['town', 'flat_type', 'storey_range', 'flat_model', 'floor_area_sqm', 'lease_commence_date', 'reg_year', 'reg_month', 'street_name', 'remaining_lease_years']

selected_options = {}

st.sidebar.markdown(
    "<h2 style='color: #FF6347;'>Select Options to Predict</h2>",
    unsafe_allow_html=True
)
for feature in features_list:
    if feature == 'town':
        selected_options[feature] = st.sidebar.selectbox(f"Select {feature.replace('_', ' ').capitalize()}:",
                                                         options=town_encoder.classes_)
    elif feature == 'storey_range':
        selected_options[feature] = st.sidebar.selectbox(f"Select {feature.replace('_', ' ').capitalize()}:",
                                                         options=storey_range_encoder.classes_)
    elif feature == 'flat_type':
        selected_options[feature] = st.sidebar.selectbox(f"Select {feature.replace('_', ' ').capitalize()}:",
                                                         options=flat_type_encoder.classes_)
    elif feature == 'flat_model':
        selected_options[feature] = st.sidebar.selectbox(f"Select {feature.replace('_', ' ').capitalize()}:",
                                                         options=flat_model_encoder.classes_)
    elif feature == 'street_name':
        selected_options[feature] = st.sidebar.selectbox(f"Select {feature.replace('_', ' ').capitalize()}:",
                                                         options=street_name_encoder.classes_)
    elif feature == 'floor_area_sqm':
        selected_options[feature] = st.sidebar.slider(f"Select {feature.replace('_', ' ').capitalize()}:",
                                                      min_value=0, max_value=500, value=100)
    elif feature in ['lease_commence_date', 'reg_year']:
        selected_options[feature] = st.sidebar.slider(f"Select {feature.replace('_', ' ').capitalize()}:",
                                                      min_value=1999, max_value=2017, value=2000)
    elif feature == 'reg_month':
        selected_options[feature] = st.sidebar.selectbox(f"Select {feature.replace('_', ' ').capitalize()}:",
                                                         options=list(range(1, 13)))
    elif feature == 'remaining_lease_years':
        selected_options[feature] = st.sidebar.slider(f"Enter {feature.replace('_', ' ').capitalize()}:",
                                                      min_value=0, max_value=99, value=50)
    else:
        selected_options[feature] = st.sidebar.text_input(f"Enter {feature.replace('_', ' ').capitalize()}:")

# Encode categorical features
selected_options['town'] = town_encoder.transform([selected_options['town']])[0]
selected_options['flat_type'] = flat_type_encoder.transform([selected_options['flat_type']])[0]
selected_options['storey_range'] = storey_range_encoder.transform([selected_options['storey_range']])[0]
selected_options['flat_model'] = flat_model_encoder.transform([selected_options['flat_model']])[0]
selected_options['street_name'] = street_name_encoder.transform([selected_options['street_name']])[0]

# Make predictions using the loaded model
if st.sidebar.button("Predict"):
    input_array = np.array([selected_options[feature] for feature in features_list]).reshape(1, -1)
    print("Input Array:", input_array)  # Print input array for debugging
    prediction = model.predict(input_array)
    # Display the prediction resul
    st.markdown(f'<span style="color:lightgreen; font-size:24px;"><b>The predicted house price is :  {prediction[0]:,.2f} INR</b></span>', unsafe_allow_html=True)

