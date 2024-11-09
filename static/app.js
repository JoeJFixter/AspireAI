// Function to call the OpenAI API via your Flask backend
function getOpenAIResponse(userInput) {
    fetch('http://127.0.0.1:5000/api/openai_api', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input: userInput })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('OpenAI response:', data.response);
        } else {
            console.error('Error from OpenAI API:', data.message);
        }
    })
    .catch(error => console.error('Error calling backend:', error));
}

// Ensure the DOM is fully loaded before adding the event listener
document.addEventListener('DOMContentLoaded', function() {
    console.log("Loaded page");
    // Event listener for form submission
    document.getElementById('queryForm').addEventListener('submit', function(event) {
        console.log("submit pressed");
        event.preventDefault(); // Prevent the default form submission behavior

        // Get the value of the input field
        const userInput = document.getElementById('userInput').value;
        console.log('User input:', userInput);
        // Call the function to send the request
        getOpenAIResponse(userInput);
    });
});
