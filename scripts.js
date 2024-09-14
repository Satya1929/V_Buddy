document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('upload-form');
    const fileUpload = document.getElementById('file-upload');
    const uploadStatus = document.getElementById('upload-status');
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const responseBox = document.getElementById('response-box');

    uploadForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData();
        formData.append('file', fileUpload.files[0]);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                uploadStatus.textContent = `File uploaded successfully: ${result.fileName}`;
            } else {
                uploadStatus.textContent = 'Failed to upload file.';
            }
        } catch (error) {
            uploadStatus.textContent = 'An error occurred while uploading the file.';
        }
    });

    sendBtn.addEventListener('click', async () => {
        const message = userInput.value;

        if (!message.trim()) {
            alert('Please enter a message.');
            return;
        }

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });

            if (response.ok) {
                const result = await response.json();
                responseBox.textContent = `Model response: ${result.response}`;
            } else {
                responseBox.textContent = 'Failed to get response from model.';
            }
        } catch (error) {
            responseBox.textContent = 'An error occurred while getting response.';
        }
    });
});
