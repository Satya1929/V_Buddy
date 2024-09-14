import google.generativeai as genai
import os

# Fetch the API key from the environment variable 'GOOGLE_API_KEY'
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Check if the API key was retrieved properly
if GOOGLE_API_KEY is None:
    raise ValueError("API Key not found in environment variables")

# Configure the Generative AI API with the fetched API key
genai.configure(api_key=GOOGLE_API_KEY)

# Function to delete all files
def delete_all_files():
    try:
        # Retrieve the list of existing files
        existing_files = genai.list_files()
        
        if not existing_files:
            print("No files found to delete.")
        else:
            for file in existing_files:
                try:
                    # Delete the file
                    genai.delete_file(file.name)  # Pass the file name to delete
                    print(f"Deleted file '{file.display_name}' with URI: {file.uri}")
                except Exception as e:
                    print(f"Failed to delete file '{file.display_name}': {str(e)}")
    
    except Exception as e:
        print(f"Failed to list files: {str(e)}")

# Delete all uploaded files
delete_all_files()
