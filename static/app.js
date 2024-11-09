// Function to call the OpenAI API via your Flask backend
function getOpenAIResponse(userInput) {
    fetch('http://127.0.0.1:5000/api/chatbot_agent_api', {
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


// Function to call the OpenAI API via your Flask backend
function getStory() {
    fetch('http://127.0.0.1:5000/api/story_agent_api', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
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

// Function to call the OpenAI API via your Flask backend
function store_basic_info(firstName, lastName, gender, age, country) {
    fetch('http://127.0.0.1:5000/api/add_basic_info', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ firstName, lastName, gender, age , country})
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
    // console.log("Loaded page");

    document.getElementById('BasicInfo').addEventListener('submit', function(event){
        event.preventDefault();
        console.log("Basic Info form submitted");
        const firstName = document.getElementById('firstName').value;
        const lastName = document.getElementById('lastName').value;
        const gender = document.getElementById("gender").value;
        const age = document.getElementById("age").value;
        const country = document.getElementById("country").value;
        store_basic_info(firstName, lastName, gender, age, country);
    });


    // Event listener for form submission for Query Form
    document.getElementById('queryForm').addEventListener('submit', function(event) {
        // console.log("submit pressed");
        event.preventDefault(); // Prevent the default form submission behavior

        // Get the value of the input field
        const userInput = document.getElementById('userInput').value;
        console.log('User input:', userInput);
        // Call the function to send the request
        getOpenAIResponse(userInput);
    });


    document.getElementById('storyForm').addEventListener('submit', function(event) {
        // console.log("submit pressed");
        event.preventDefault(); // Prevent the default form submission behavior

        // Call the function to send the request
        getStory();
    });
});
