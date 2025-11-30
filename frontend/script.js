document.getElementById('correctBtn').addEventListener('click', () => {
    const codeInput = document.getElementById('codeInput').value;
    const codeOutput = document.getElementById('codeOutput');
    
    codeOutput.textContent = 'Correcting...';

    fetch('http://127.0.0.1:8000/api/correct', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: codeInput }),
    })
    .then(response => response.json())
    .then(data => {
        codeOutput.textContent = data.corrected_code;
    })
    .catch(error => {
        console.error('Error:', error);
        codeOutput.textContent = '# An error occurred while connecting to the API.';
    });
});