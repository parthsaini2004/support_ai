// src/utils/chatAPI.js
// This file contains the API call to send messages to the backend
import axios from 'axios';

export const sendMessageToBackend = async (message) => {
  const res = await axios.post('http://localhost:5000/api/query', { message });
  return res.data;
};
