import React, { useState } from "react";
import ChatWindow from "../components/ChatWindow";
import InputBox from "../components/InputBox";
import { sendMessageToBackend } from "../utils/chatAPI";

const ChatPage = () => {
  const [messages, setMessages] = useState([]);

  const handleSend = async (userMessage) => {
    const userMsg = { sender: "user", text: userMessage };
    setMessages((prev) => [...prev, userMsg]);

    const aiResponse = await sendMessageToBackend(userMessage);
    const aiMsg = { sender: "ai", text: aiResponse };

    setMessages((prev) => [...prev, aiMsg]);
  };

  return (
    <div className="flex flex-col h-screen">
      <ChatWindow messages={messages} />
      <InputBox onSend={handleSend} />
    </div>
  );
};

export default ChatPage;
