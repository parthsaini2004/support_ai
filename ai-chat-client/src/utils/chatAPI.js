export const sendMessageToBackend = async (message) => {
  try {
    // Get the token from localStorage or cookies
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
