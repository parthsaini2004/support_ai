import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const Signin = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    const baseURL = import.meta.env.VITE_API_BASE_URL; // Make sure to replace with actual base URL
    const userData = { email, password };

    try {
      // Send request to backend with email and password
      const response = await axios.post(`${baseURL}/api/signin`, userData, {
        headers: {
          "Content-Type": "application/json",
        },
        withCredentials: true, // Ensure that cookies are included in the request
      });

      const { token, user } = response.data; // Get token and user details from response

      // Store token in localStorage
      localStorage.setItem("token", token);

      // Optionally store user details, like user_id, if you need it
      localStorage.setItem("user_id", user.user_id);

      // Display success message
      setSuccess("Logged in successfully!");

      // Reset form values
      setEmail("");
      setPassword("");

      // Navigate to the next page (e.g., chat)
      navigate("/chat");
    } catch (err) {
      console.error("Signin error:", err.response?.data || err.message);
      setError(err.response?.data?.error || "Something went wrong!");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 px-4">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-lg p-8 space-y-6">
        <h2 className="text-2xl font-bold text-center text-gray-800">Sign In</h2>

        {error && (
          <div className="bg-red-100 text-red-700 px-4 py-2 rounded-md text-sm">
            {error}
          </div>
        )}
        {success && (
          <div className="bg-green-100 text-green-700 px-4 py-2 rounded-md text-sm">
            {success}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="mt-1 w-full px-4 py-2 border rounded-lg shadow-sm focus:ring focus:ring-blue-200 focus:outline-none"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="mt-1 w-full px-4 py-2 border rounded-lg shadow-sm focus:ring focus:ring-blue-200 focus:outline-none"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white font-semibold py-2 rounded-lg hover:bg-blue-700 transition duration-200"
          >
            Sign In
          </button>
        </form>
      </div>
    </div>
  );
};

export default Signin;
