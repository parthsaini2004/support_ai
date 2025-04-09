import { spawn } from "child_process";
import path from "path";

// Utility to run Python subprocess
export const runPythonAgent = (userInput) => {
  return new Promise((resolve, reject) => {
    const pythonPath = path.join(process.cwd(), "langchain/langchain_agent.py");  // Path to Python script

    const process = spawn("python3", [pythonPath]);  // Run the Python script

    let result = "";

    // Capture output from Python process
    process.stdout.on("data", (data) => {
      result += data.toString();
    });

    // Capture error output from Python process
    process.stderr.on("data", (data) => {
      console.error(`Python error: ${data}`);
    });

    // Write the user input as JSON to the Python process
    process.stdin.write(JSON.stringify({ message: userInput }));
    process.stdin.end();

    // Resolve the result when the Python process ends
    process.on("close", () => {
      resolve(result.trim());
    });
  });
};
