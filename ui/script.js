// script.js

// Function to send message
async function sendMessage() {
    const userInput = document.getElementById("user-input");
    const message = userInput.value.trim();
  
    if (message === "") return;
  
    addMessageToChat(message, "user");
  
    // Clear input field
    userInput.value = "";
  
    // Call backend to get the bot's response
    const botResponse = await getBotResponse(message);
  
    // Display bot response
    addMessageToChat(botResponse, "bot");
  }
  
  // Function to add message to chat box
  function addMessageToChat(message, sender) {
    const chatBox = document.getElementById("chat-box");
  
    const messageElement = document.createElement("div");
    messageElement.classList.add("message");
    if (sender === "user") {
      messageElement.classList.add("user-message");
      messageElement.innerText = message;
    } else {
      messageElement.classList.add("bot-message");
      messageElement.innerText = message;
    }
  
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
  }
  
  // Function to call backend API and get bot response
  async function getBotResponse(message) {
    try {
      const response = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: message })
      });
      const data = await response.json();
      return data.answer || "Sorry, I couldn't find an answer.";
    } catch (error) {
      console.error("Error fetching response:", error);
      return "There was an error getting the response. Please try again.";
    }
  }
  