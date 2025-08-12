import React, { useState } from "react";
import ChatWindow from "../components/ChatWindow";
import InputBox from "../components/InputBox";

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [thinking, setThinking] = useState(false);

  // Define the function inside ChatPage component
  const sendMessageToBackend = async (message) => {
    try {
      // Get the token from localStorage
      const token = localStorage.getItem("token");  // Assuming the token is stored in localStorage

      const response = await fetch("http://localhost:5001/api/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,  // Include token in the request header
        },
        credentials: "include", 
        body: JSON.stringify({ query: message }),  // Pass 'query' as the field instead of 'message'
      });

      const data = await response.json();
      return data.response;
    } catch (error) {
      console.error("Error communicating with backend:", error);
      return "⚠️ Something went wrong!";
    }
  };

  const handleSend = async (userMessage) => {
    const userMsg = { sender: "user", text: userMessage };
    setMessages((prev) => [...prev, userMsg]);

     // Add thinking message
     const thinkingMsg = { sender: "ai", text: "🤔 Thinking..." };
     setMessages((prev) => [...prev, thinkingMsg]);
     setThinking(true);

    const aiResponse = await sendMessageToBackend(userMessage);

    setMessages((prev) => {
      const updated = [...prev];
      updated[updated.length - 1] = { sender: "ai", text: aiResponse };
      return updated;
    });

    setThinking(false);

    // const aiMsg = { sender: "ai", text: aiResponse };

    // setMessages((prev) => [...prev, aiMsg]);
  };

  return (
    <div className="flex flex-col h-screen">
      <ChatWindow messages={messages} />
      <InputBox onSend={handleSend} />
    </div>
  );
};

export default ChatPage;
