export const sendMessageToBackend = async (message) => {
  try {
    const response = await fetch("http://localhost:5001/api/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include", 
      body: JSON.stringify({ message }),
    });

    const data = await response.json();
    return data.response;
  } catch (error) {
    console.error("Error communicating with backend:", error);
    return "⚠️ Something went wrong!";
  }
};
