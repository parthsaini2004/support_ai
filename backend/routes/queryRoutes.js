import express from "express";
import { spawn } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const router = express.Router();

// __dirname fix for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Update the Python file path if it's in the 'langchain' folder
router.post("/query", async (req, res) => {
  const userMessage = req.body.message;

  // Make sure the path to langchain_agent.py is correct
  const python = spawn("python3", [path.join(__dirname, "..", "langchain", "langchain_agent.py")]);

  python.stdin.write(JSON.stringify({ message: userMessage }));
  python.stdin.end();

  let responseData = "";

  python.stdout.on("data", (data) => {
    responseData += data.toString();
  });

  python.stderr.on("data", (data) => {
    console.error(`stderr: ${data}`);
  });

  python.on("close", (code) => {
    try {
      const result = JSON.parse(responseData);
      const inner = typeof result === "string" ? JSON.parse(result) : result;
      res.json({ response: inner.response });
    } catch (error) {
      console.error("Error parsing response:", error);
      res.status(500).json({ response: "AI agent failed to respond." });
    }
  });
});

export default router;
