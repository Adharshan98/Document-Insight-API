document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('qa-form');
    const fileInput = document.getElementById('file-input');
    const fileNameDisplay = document.getElementById('file-name');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const spinner = submitBtn.querySelector('.spinner');
    
    const resultContainer = document.getElementById('result-container');
    const answerText = document.getElementById('answer-text');
    const chunksUsed = document.getElementById('chunks-used');
    const errorMessage = document.getElementById('error-message');

    // Update file name on selection
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            fileNameDisplay.textContent = e.target.files[0].name;
            fileNameDisplay.style.color = 'var(--text-main)';
        } else {
            fileNameDisplay.textContent = 'Click to upload or drag and drop';
            fileNameDisplay.style.color = 'var(--text-secondary)';
        }
    });

    // Handle Form Submit
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // 1. Reset State
        errorMessage.classList.add('hidden');
        errorMessage.textContent = '';
        resultContainer.classList.add('hidden');
        
        // 2. Loading State
        submitBtn.disabled = true;
        btnText.textContent = 'Processing...';
        spinner.classList.remove('hidden');

        // 3. Prepare Data
        const formData = new FormData(form);

        try {
            // 4. API Call
            const response = await fetch("http://127.0.0.1:8000/qa/", {
                method: "POST",
                body: formData
            });

            if (!response.ok) {
                // Try to get error message from backend
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `Server Error: ${response.status}`);
            }

            const data = await response.json();

            // 5. Display Result
            answerText.textContent = data.answer;
            chunksUsed.textContent = data.chunks_used || 0;
            resultContainer.classList.remove('hidden');

        } catch (error) {
            console.error('API Error:', error);
            errorMessage.textContent = error.message || 'Failed to connect to the server. Please ensure the backend is running.';
            errorMessage.classList.remove('hidden');
        } finally {
            // 6. Reset Button State
            submitBtn.disabled = false;
            btnText.textContent = 'Get Answer';
            spinner.classList.add('hidden');
        }
    });
});
