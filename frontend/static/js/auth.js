document.getElementById('registerForm').addEventListener('submit', async (e) => {
    const username = document.getElementById('username').value;
    const email_address = document.getElementById('email').value;
    const password = document.getElementById('pwd').value;
    e.preventDefault()
    try {
        const response = await fetch('http://127.0.0.1:8000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email_address, password })
        });

        const data = await response.json();
        
        if (response.ok) {
            alert('Registration successful!');
        } else {
            alert('Error: ' + data.detail);
        }
    } catch (error) {
        console.error('Error:', error);
    }
});