import streamlit as st
import pandas as pd
import numpy as np
from src.pipeline.predict_pipeline import CustomData, PredictPipeline


# Title
st.title("📚 Student Performance Prediction App")

# Sidebar with a Form
with st.sidebar.form("student_form", clear_on_submit=False):
    st.header("Enter Student Details:")

    gender = st.selectbox("Gender", ["male", "female"])
    race_ethnicity = st.selectbox("Race/Ethnicity", ["group A", "group B", "group C", "group D", "group E"])
    parental_level_of_education = st.selectbox(
        "Parental Level of Education",
        [
            "some high school",
            "high school",
            "some college",
            "associate's degree",
            "bachelor's degree",
            "master's degree"
        ]
    )
    lunch = st.selectbox("Lunch", ["standard", "free/reduced"])
    test_preparation_course = st.selectbox("Test Preparation Course", ["none", "completed"])
    reading_score = st.number_input("Reading Score", min_value=0, max_value=100)
    writing_score = st.number_input("Writing Score", min_value=0, max_value=100)
    math_score = st.number_input("Math Score (Optional if known)", min_value=0, max_value=100)

    # Submit button inside the form
    submit = st.form_submit_button("Predict Student Performance")

# After form is submitted
if submit:
    try:
        # Prepare input
        input_data = CustomData(
            gender=gender,
            race_ethnicity=race_ethnicity,
            parental_level_of_education=parental_level_of_education,
            lunch=lunch,
            test_preparation_course=test_preparation_course,
            reading_score=reading_score,
            writing_score=writing_score
        )
        
        data_frame = input_data.get_data_as_data_frame()
        
        # Predict Math Score
        predict_pipeline = PredictPipeline()
        predicted_math_score = predict_pipeline.predict(data_frame)[0]

        # Use entered Math Score if available
        final_math_score = math_score if math_score > 0 else predicted_math_score

        # Predict other scores (simple rule)
        predicted_reading_score = max(min(final_math_score + 5, 100), 0)
        predicted_writing_score = max(min(final_math_score + 7, 100), 0)

        # Total Score
        total_score = final_math_score + predicted_reading_score + predicted_writing_score

        # Display results
        st.success(f"Predicted Math Score: {final_math_score:.2f}")
        st.info(f"Estimated Reading Score: {predicted_reading_score:.2f}")
        st.info(f"Estimated Writing Score: {predicted_writing_score:.2f}")
        st.success(f"Total Score (Math + Reading + Writing): {total_score:.2f}")

    except Exception as e:
        st.error(f"❗ Error: {e}")

# Footer
st.write("---")
st.caption("Developed by [Harsh Wasnik]")
