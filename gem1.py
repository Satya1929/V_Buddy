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

################################################################################################# upload and verify

# Path to your local PDF file (update this path to point to your actual file)
local_file_path = r"C:\Users\ASUS\Desktop\nptel_forest_fat_exam_guide_1.pdf"
file_display_name = "nptel fat 1 PDF"

# Check if the file already exists (same file name check onlyand not inside content)
sample_file = None  # Initialize sample_file to None
try:
    # Retrieve the list of existing files
    existing_files = genai.list_files()  # Adjust this based on your API

    # Check if the file with the same display name exists
    for file in existing_files:
        if file.display_name == file_display_name:
            sample_file = file
            break

    if sample_file:
        print("File exists, so continue next steps")
    else:
        # Upload the file
        sample_file = genai.upload_file(path=local_file_path, display_name=file_display_name)

        # Print the file URI for reference
        print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

        # Update the list of existing files
        existing_files = genai.list_files()  # Retrieve updated list

        # Verify PDF file upload and get metadata
        try:
            # Retrieve file metadata using the uploaded file's name
            file = genai.get_file(name=sample_file.name)

            # Print file details
            print(f"Retrieved file '{file.display_name}' as: {file.uri}")
        except Exception as e:
            print(f"Failed to retrieve file metadata: {str(e)}")

except Exception as e:
    print(f"Failed to check existing files: {str(e)}")


##################################################################################################

# Loop to repeatedly ask questions until the user says "exit"
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Exiting the conversation.")
        break
    try:
        # Prompt the model with the user input and the previously uploaded file
        response = model.generate_content([sample_file, user_input])

        # Print the model's response
        print(f"Model: {response.text}")
    except Exception as e:
        print(f"Failed to generate content: {str(e)}")
