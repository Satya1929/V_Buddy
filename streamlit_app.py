import streamlit as st
import google.generativeai as genai
import os

# Fetch the API key from the environment variable 'GOOGLE_API_KEY'
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Check if the API key was retrieved properly
if GOOGLE_API_KEY is None:
    st.error("API Key not found in environment variables")
    st.stop()

# Configure the Generative AI API with the fetched API key
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to upload and verify multiple files
def upload_and_verify_files(file_paths):
    uploaded_files = []  # List to store uploaded files
    try:
        # Retrieve the list of existing files
        existing_files = genai.list_files()  # Adjust this based on your API

        for file_path in file_paths:
            file_display_name = os.path.basename(file_path)

            # Check if the file with the same display name exists
            sample_file = None
            for file in existing_files:
                if file.display_name == file_display_name:
                    sample_file = file
                    break

            if sample_file:
                st.warning(f"File '{file_display_name}' already exists, skipping upload.")
            else:
                # Upload the file if it doesn't exist
                sample_file = genai.upload_file(path=file_path, display_name=file_display_name)
                st.success(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

            # Add the file to the uploaded_files list
            uploaded_files.append(sample_file)

        # Return the list of uploaded files
        return uploaded_files

    except Exception as e:
        st.error(f"Failed to upload or verify files: {str(e)}")
        return []

# Streamlit app layout
st.title("Generative AI File Upload and Interaction")

# Keep track of all uploaded files (even from previous sessions)
if "all_uploaded_files" not in st.session_state:
    st.session_state.all_uploaded_files = []

# File uploader widget in Streamlit
uploaded_files_streamlit = st.file_uploader("Choose PDF files (OCR enabled)", accept_multiple_files=True, type=["pdf"])

if uploaded_files_streamlit:
    # Saving files to temporary directory
    file_paths = []
    for uploaded_file in uploaded_files_streamlit:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        file_paths.append(uploaded_file.name)

    # Upload and verify files through the API
    newly_uploaded_files = upload_and_verify_files(file_paths)

    # Append new files to session state
    st.session_state.all_uploaded_files.extend(newly_uploaded_files)

# Display all uploaded files, including previous ones
if st.session_state.all_uploaded_files:
    st.write("Previously and newly uploaded files:")
    for file in st.session_state.all_uploaded_files:
        st.write(f"- {file.display_name}")

# Text input for user prompt
user_input = st.text_input("Ask a question to the model:", "")

if user_input and st.session_state.all_uploaded_files:
    try:
        # Prompt the model with the user input and the previously uploaded files
        prompt = [user_input] + st.session_state.all_uploaded_files
        response = model.generate_content(prompt)

        # Display the model's response
        st.write(f"Model: {response.text}")
    except Exception as e:
        st.error(f"Failed to generate content: {str(e)}")
