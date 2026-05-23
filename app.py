# Partha Bhowmick IITKGP 2026 May 23

import streamlit as st
import os
import pandas as pd

# Set page to wide mode for better image grids
st.set_page_config(layout="wide", page_title="ICVGIP'26 Mandala Evaluation")

# 1. Initialize variables in Session State
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "scores" not in st.session_state:
    st.session_state.scores = {}

# 2. Get list of images
IMAGE_DIR = "images"
# Filters for png/jpg, ignoring the placeholder.txt
if os.path.exists(IMAGE_DIR):
    image_files = [f for f in os.listdir(IMAGE_DIR) if f.endswith(('.png', '.jpg', '.jpeg'))]
    image_files.sort()
else:
    image_files = []

# 3. Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["1. User Details", "2. Rate Mandalas", "3. Submit"])

# --- PAGE 1: USER DETAILS ---
if page == "1. User Details":
    st.title("Rater Information")
    st.write("Please provide your details before starting the evaluation.")

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.user_data['Name'] = st.text_input("Name", st.session_state.user_data.get('Name', ''))
        st.session_state.user_data['Email'] = st.text_input("Email", st.session_state.user_data.get('Email', ''))
        st.session_state.user_data['Age'] = st.number_input("Age", min_value=18, max_value=100, step=1, value=st.session_state.user_data.get('Age', 25))
    with col2:
        st.session_state.user_data['Gender'] = st.selectbox("Gender", ["Select...", "Female", "Male", "Other", "Prefer not to say"], index=0)
        st.session_state.user_data['Country'] = st.text_input("Country", st.session_state.user_data.get('Country', ''))
        occupation_options = [
            "Select...",
            "School Student",
            "College Student",
            "Industry",
            "Academia",
            "Home Development",
            "None"
        ]
        # Find the previous index to maintain state, or default to 0 ("Select...")
        try:
            default_occ_index = occupation_options.index(st.session_state.user_data.get('Occupation', 'Select...'))
        except ValueError:
            default_occ_index = 0

        # FIXED: Indented correctly to stay inside the col2 block
        st.session_state.user_data['Occupation'] = st.selectbox(
            "Occupation",
            options=occupation_options,
            index=default_occ_index
        )

    # FIXED: Indented to align with col1 and col2, escaping the 'with col2:' block
    st.session_state.user_data['Additional Info'] = st.text_area("Additional Info (Optional)", st.session_state.user_data.get('Additional Info', ''))

# --- PAGE 2: IMAGE GRID ---
elif page == "2. Rate Mandalas":
    st.title("Mandala Evaluation (0 = Worst, 10 = Best)")

    if not image_files:
        st.warning("No images found in the 'images' folder.")
    else:
        # Create a 2x2 grid dynamically
        cols_per_row = 2
        for i in range(0, len(image_files), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                if i + j < len(image_files):
                    img_name = image_files[i + j]
                    img_path = os.path.join(IMAGE_DIR, img_name)

                    with col:
                        # Display the image tightly
                        st.image(img_path, use_container_width=True)

                        # Display the slider
                        current_score = st.session_state.scores.get(img_name, 5) # Default to 5
                        score = st.slider(f"Score for {img_name}", 0, 10, current_score, key=f"slider_{img_name}")
                        st.session_state.scores[img_name] = score
            st.divider() # Visual break between rows

# --- PAGE 3: SUBMIT ---
elif page == "3. Submit":
    st.title("Review and Submit")
    st.write("Thank you for completing the evaluation. Please download your results and return them.")

    # Combine user data and scores into one dictionary
    final_data = {**st.session_state.user_data, **st.session_state.scores}
    df = pd.DataFrame([final_data])

    st.dataframe(df) # Shows a preview of the data

    # Convert dataframe to CSV for download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download My Scores (CSV)",
        data=csv,
        file_name="mandala_evaluation_scores.csv",
        mime="text/csv",
    )

