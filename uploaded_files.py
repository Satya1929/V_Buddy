import google.generativeai as genai
import os

# Fetch the API key from the environment variable 'GOOGLE_API_KEY'
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Check if the API key was retrieved properly
if GOOGLE_API_KEY is None:
    raise ValueError("API Key not found in environment variables")

# Configure the Generative AI API with the fetched API key
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model (initialize only if needed)
# model = genai.GenerativeModel('gemini-1.5-flash') # Uncomment if you need the model instance

# Function to list and print all uploaded files
def list_uploaded_files():
    try:
        # Retrieve the list of existing files
        existing_files = genai.list_files()
        
        if not existing_files:
            print("No files found.")
        else:
            print("List of uploaded files:")
            for file in existing_files:
                print(f"Display Name: {file.display_name}, URI: {file.uri}")
    
    except Exception as e:
        print(f"Failed to list files: {str(e)}")

# List all uploaded files
list_uploaded_files()
