//queryController.js
import { runPythonAgent } from "../utils/pythonRunner";  // Import the function

export const handleQuery = async (req, res) => {
  try {
    const userMessage = req.body.message;  // Get the user input

    // Run the Python agent with the user input
    const result = await runPythonAgent(userMessage);

    // Parse the result from Python
    try {
      const parsedResult = JSON.parse(result);
      res.json({ response: parsedResult.response });  // Send back the response from the agent
    } catch (err) {
      console.error("Failed to parse Python response:", result);
      res.status(500).json({ response: "AI agent failed to respond." });
    }
  } catch (error) {
    console.error("Error:", error);
    res.status(500).json({ response: "Server error" });
  }
};
