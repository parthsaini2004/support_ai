// src/pages/Home.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();

  const handleStart = () => {
    navigate('/chat');
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center text-center bg-white">
      <h1 className="text-4xl font-bold mb-4">AI Support Agent 🤖</h1>
      <p className="mb-6 text-gray-700">Ask any questions and get instant support!</p>
      <button
        onClick={handleStart}
        className="bg-blue-600 text-white px-6 py-3 rounded-xl hover:bg-blue-700"
      >
        Start Chat
      </button>
    </div>
  );
};

export default Home;
