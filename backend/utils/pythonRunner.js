import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

/**
 * Runs a Python script with the provided arguments and returns the output
 * @param {string} scriptPath - Relative path to the Python script from project root
 * @param {Object} args - Arguments to pass to the Python script as JSON
 * @returns {Promise<string>} - Promise resolving to the script's output
 */
const runPythonScript = (scriptPath, args) => {
  return new Promise((resolve, reject) => {
    // Convert relative path to absolute
    const absolutePath = path.join(process.cwd(), scriptPath);
    
    // Spawn Python process
    const pythonProcess = spawn('python', [
      absolutePath,
      JSON.stringify(args)
    ]);
    
    let outputData = '';
    let errorData = '';

    // Collect data from stdout
    pythonProcess.stdout.on('data', (data) => {
      outputData += data.toString();
    });

    // Collect error data from stderr
    pythonProcess.stderr.on('data', (data) => {
      errorData += data.toString();
    });

    // Handle process completion
    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Python script exited with code ${code}: ${errorData}`));
      } else {
        try {
          // Try to parse the output as JSON
          const jsonOutput = JSON.parse(outputData);
          resolve(jsonOutput);
        } catch (e) {
          // If not valid JSON, return the raw output
          resolve(outputData);
        }
      }
    });

    // Handle process errors
    pythonProcess.on('error', (error) => {
      reject(new Error(`Failed to start Python process: ${error.message}`));
    });
  });
};

export default runPythonScript;