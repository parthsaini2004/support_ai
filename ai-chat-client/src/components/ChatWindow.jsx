// src/components/ChatWindow.jsx
import React from 'react';
import MessageBubble from './MessageBubble';

const ChatWindow = ({ messages }) => {
  return (
    <div className="flex-1 overflow-y-auto px-4 py-4">
      {messages.map((msg, index) => (
        <MessageBubble key={index} sender={msg.sender} text={msg.text} />
      ))}
    </div>
  );
};

export default ChatWindow;
