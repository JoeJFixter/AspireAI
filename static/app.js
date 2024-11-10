// Function to call the OpenAI API via your Flask backend
const chatInput = document.getElementById("chat-input");
       const sendButton = document.getElementById("send-button");
       const previousChat = document.getElementById("previous-chat");

   
function addAgentMessageToChat(message) {
    const messageBubble = document.createElement("div");
    messageBubble.classList.add("mb-2", "text-left");

    const bubbleContent = document.createElement("div");
    bubbleContent.classList.add("bg-green-100", "text-blue-800", "p-2", "rounded-lg", "w-max", "max-w-xs");
    bubbleContent.textContent = message;

    messageBubble.appendChild(bubbleContent);
    previousChat.appendChild(messageBubble);

    previousChat.scrollTop = previousChat.scrollHeight; // Ensure scrolled to top of conversation.
}

       // Event listener for the Enter key
       chatInput.addEventListener("keypress", (event) => {
           if (event.key === "Enter") {
               const message = chatInput.value.trim();
               if (message) {
                   addMessageToChat(message);
                   chatInput.value = ""; // Clear input after sending
                   event.preventDefault();
               
               }
           }
       });
     






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
            addAgentMessageToChat(data.response);
        } else {
            console.error('Error from OpenAI API:', data.message);
        }
    })
    .catch(error => console.error('Error calling backend:', error));
}


// // Function to call the OpenAI API via your Flask backend
// function getStory() {
//     fetch('http://127.0.0.1:5000/api/story_agent_api', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({})
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.status === 'success') {
//             console.log('OpenAI response:', data.response);
//             return data.response;
//         } else {
//             console.error('Error from OpenAI API:', data.message);
//         }
//     })
//     .catch(error => console.error('Error calling backend:', error));
// }

function getStory() {
    return fetch('http://127.0.0.1:5000/api/story_agent_api', {
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
            return data.response; // Resolve the Promise with the API response
        } else {
            console.error('Error from OpenAI API:', data.message);
            throw new Error(data.message); // Reject the Promise with an error
        }
    })
    .catch(error => {
        console.error('Error calling backend:', error);
        throw error; // Propagate the error to be handled by .catch in the calling code
    });
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

// Function to call the OpenAI API via your Flask backend
function getTasks() {
    fetch('http://127.0.0.1:5000/api/task_agent_api', {
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
            alert("Sent to your google calendar");

        } else {
            console.error('Error from OpenAI API:', data.message);
        }
    })
    .catch(error => console.error('Error calling backend:', error));
}

// Ensure the DOM is fully loaded before adding the event listener

    // console.log("Loaded page");

    // document.getElementById('BasicInfo').addEventListener('submit', function(event){
    function get_user_info(){
        console.log("Basic Info form submitted");
        const firstName = document.getElementById('firstName').value;
        const lastName = document.getElementById('lastName').value;
        const gender = document.getElementById("gender").value;
        const age = document.getElementById("age").value;
        const country = document.getElementById("country").value;
        const occupation = document.getElementById("Occupation").value;
        const employmentType = document.getElementById("employmentType").value;
        store_basic_info(firstName, lastName, gender, age, country, occupation, employmentType);
    };


    // Event listener for form submission for Query Form
    // document.getElementById('queryForm').addEventListener('submit', function(event) {
    function get_response(message){
        // console.log("submit pressed");
        event.preventDefault(); // Prevent the default form submission behavior

        // Get the value of the input field
        // const userInput = document.getElementById('userInput').value;
        // console.log('User input:', userInput);
        // Call the function to send the request
        getOpenAIResponse(message);
    }


    // document.getElementById('storyForm').addEventListener('submit', function(event) {
    // function get_story(){
    //     // console.log("submit pressed");
    //     event.preventDefault(); // Prevent the default form submission behavior

    //     // Call the function to send the request
    //     getStory();
    // });


    // document.getElementById('tasksForm').addEventListener('submit', function(event) {
    //     // console.log("submit pressed");
    //     event.preventDefault(); // Prevent the default form submission behavior

    //     // Call the function to send the request
    //     getTasks();
    // });

    function addMessageToChat(message) {
        const messageBubble = document.createElement("div");
        
        messageBubble.classList.add("flex-1" ,"p-2" ,"overflow-y-auto");


        const bubbleContent = document.createElement("div");
        
        bubbleContent.classList.add("bg-green-100", "text-green-800","p-3", "rounded-lg", "w-max", "max-w-xs","mb-1", "ml-auto");
        bubbleContent.textContent = message;

        messageBubble.appendChild(bubbleContent);
        
        previousChat.appendChild(messageBubble);

        
        previousChat.scrollTop = previousChat.scrollHeight; //Ensure scrolled to top of conversation.

        get_response(message);
    }


    function openMission() {
        document.getElementById("missionForm").style.display = "block";
  
      }
      function closeMission() {
        document.getElementById("missionForm").style.display = "none";
  
      }
         
      function openPipeline() {
        document.getElementById("pipelineModal").style.display = "block";
  
      }
      function closePipeline() {
        document.getElementById("pipelineModal").style.display = "none";
  
      }
    function openStory() {
      getStory().then(story_text => {
        console.log(story_text);
        document.getElementById("storyText").innerHTML = story_text;
        document.getElementById("storyModal").style.display = "block";
      });
    }
      function closeStory() {
        document.getElementById("storyModal").style.display = "none";
      }

    sendButton.addEventListener("click", () => {
        const message = chatInput.value.trim();
        if (message) {
            addMessageToChat(message);
            chatInput.value = ""; 
        }
    });




