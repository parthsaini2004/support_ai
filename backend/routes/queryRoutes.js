// queryRoutes.js
import express from "express";
import { spawn } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const router = express.Router();

// __dirname fix for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// POST route to handle AI agent query
router.post("/query", async (req, res) => {
  const userMessage = req.body.message;
  const userId = req.body.user_id;

  // Make sure the path to langchain_agent.py is correct
  const python = spawn("python3", [
    path.join(__dirname, "..", "langchain", "langchain_agent.py"),
  ]);

  // ✅ Pass both message and user_id to the Python script
  python.stdin.write(
    JSON.stringify({
      message: userMessage,
      user_id: userId,
    })
  );
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
