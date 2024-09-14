import google.generativeai as genai
import os

# Fetch the API key from the environment variable 'GOOGLE_API_KEY'
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Check if the API key was retrieved properly
if GOOGLE_API_KEY is None:
    raise ValueError("API Key not found in environment variables")

# Configure the Generative AI API with the fetched API key
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to calculate the size of a file
def get_file_size(file_path):
    return os.path.getsize(file_path)

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
                print(f"File '{file_display_name}' already exists, skipping upload.")
            else:
                # Upload the file if it doesn't exist
                sample_file = genai.upload_file(path=file_path, display_name=file_display_name)
                print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

            # Add the file to the uploaded_files list
            uploaded_files.append(sample_file)

        # Return the list of uploaded files
        return uploaded_files

    except Exception as e:
        print(f"Failed to upload or verify files: {str(e)}")
        return []

# List of paths to your local PDF files (update these paths with your actual files)
# upload only the OCR enabled pdf files
file_paths = [
    r"C:\Users\ASUS\Desktop\da1.pdf",
    r"C:\Users\ASUS\Desktop\nptel_forest_fat_exam_guide_1.pdf",
    r"C:\Users\ASUS\Desktop\Acad_calender.pdf"  
    # Add more file paths here
]

# Upload and verify the files
uploaded_files = upload_and_verify_files(file_paths)

##################################################################################################

# Loop to repeatedly ask questions until the user says "exit"
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Exiting the conversation.")
        break
    try:
        # Prompt the model with the user input and the previously uploaded files
        prompt = [user_input] + uploaded_files
        response = model.generate_content(prompt)

        # Print the model's response
        print(f"Model: {response.text}")
    except Exception as e:
        print(f"Failed to generate content: {str(e)}")
