// src/components/InputBox.jsx
import React, { useState } from 'react';

const InputBox = ({ onSend }) => {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (!input.trim()) return;
    onSend(input);
    setInput('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleSend();
  };

  return (
    <div className="flex gap-2 p-4 border-t">
      <input
        type="text"
        placeholder="Type your message..."
        className="flex-1 border rounded-xl px-4 py-2 text-sm focus:outline-none"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
      />
      <button
        onClick={handleSend}
        className="bg-blue-500 text-white px-4 py-2 rounded-xl text-sm hover:bg-blue-600"
      >
        Send
      </button>
    </div>
  );
};

export default InputBox;
