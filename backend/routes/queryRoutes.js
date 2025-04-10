import express from "express";
import { spawn } from "child_process";
import path from "path";
import { fileURLToPath } from "url";
import authMiddleware from "../middleware/authMiddleware.js"; // Import the auth middleware

const router = express.Router();

// __dirname fix for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ✅ Updated /query route to send both message and user_id
router.post("/query", authMiddleware, async (req, res) => {
  console.log("✅ /query route hit"); 
  const userMessage = req.body.message;
  const userId = req.user.user_id; // ✅ Extracted from token

  // ✅ Log to terminal for debugging
  console.log("🔐 Token decoded, user ID:", userId);
  console.log("📨 Incoming user message:", userMessage);

  const python = spawn("python3", [
    path.join(__dirname, "..", "langchain", "langchain_agent.py"),
  ]);

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
    console.error(`🐍 Python stderr: ${data}`);
  });

  python.on("close", (code) => {
    try {
      const result = JSON.parse(responseData);
      const inner = typeof result === "string" ? JSON.parse(result) : result;
      res.json({ response: inner.response });
    } catch (error) {
      console.error("❌ Error parsing response from Python:", error);
      res.status(500).json({ response: "AI agent failed to respond." });
    }
  });
});



export default router;
