import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="Insurance Predictor", layout="wide")

API_URL = "http://localhost:8000/predict"

# --- UI Layout ---
st.title("🛡️ Insurance Premium Category Predictor")
st.markdown("Provide your details below to receive a personalized premium estimate.")
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Biometrics**")
    age = st.number_input("Age", min_value=1, max_value=119, value=30, step=1)
    height = st.number_input("Height (m)", min_value=0.5, max_value=2.49, value=1.70, step=0.01)
    weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0, step=0.5)

    # Keep this just for visual feedback for the user
    bmi = weight / (height ** 2)
    st.caption(f"Calculated BMI: **{bmi:.1f}**")

with col2:
    st.markdown("**Lifestyle & Demographics**")
    smoker_input = st.radio("Do you smoke?", ["No", "Yes"], horizontal=True)
    smoker = True if smoker_input == "Yes" else False
    city = st.text_input("City of Residence", value="Mumbai")

with col3:
    st.markdown("**Financials**")
    occupation_ui = st.selectbox(
        "Current Occupation",
        ['Private Job', 'Government Job', 'Business Owner', 'Freelancer', 'Student', 'Retired', 'Unemployed']
    )
    income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0, step=0.5)

st.divider()

# --- Prediction Action ---
_, center_col, _ = st.columns([1, 2, 1])

with center_col:
    if st.button("Generate Premium Quote ➔", use_container_width=True, type="primary"):

        # Map UI occupation to API allowed Literal values
        occ_map = {
            'Private Job': 'private_job', 'Government Job': 'government_job',
            'Business Owner': 'business_owner', 'Freelancer': 'freelancer',
            'Student': 'student', 'Retired': 'retired', 'Unemployed': 'unemployed'
        }

        # Payload perfectly matches your new UserInput Pydantic class
        input_data = {
            "age": age,
            "weight": weight,
            "height": height,
            "income_lpa": income_lpa,
            "smoker": smoker,
            "city": city,
            "occupation": occ_map[occupation_ui]
        }

        with st.spinner("Analyzing risk profile..."):
            try:
                response = requests.post(API_URL, json=input_data, timeout=10)

                if response.status_code == 200:
                    result = response.json()

                    # Matches your updated return dict: {'predicted_category': prediction}
                    if "predicted_category" in result:
                        cat = result['predicted_category']
                        st.success("Analysis Complete.")
                        st.metric("Predicted Premium Category", cat.upper())
                    else:
                        st.error("Unexpected API response format.")
                        st.code(result)

                # Specifically catch Pydantic validation errors (422)
                elif response.status_code == 422:
                    st.error("Validation Error: The backend rejected the inputs.")
                    st.json(response.json())
                else:
                    st.error(f"API Error: {response.status_code}")
                    st.write(response.text)

            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the server. Ensure the FastAPI app is running.")