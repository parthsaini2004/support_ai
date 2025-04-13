import { exec } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

// Get current directory name
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// ✅ One folder up: from /backend/utils → /main.py
const pythonScriptPath = path.join(__dirname, '..', 'main.py');

console.log("✅ Python path:", pythonScriptPath); // Optional debug log

export const pythonRunner = (userId, query) => {
  return new Promise((resolve, reject) => {
    exec(
      `python3 ${pythonScriptPath} --user-id ${userId} --query "${query}"`,
      (error, stdout, stderr) => {
        if (error) {
          console.error('❌ Error executing Python script:', error);
          return reject('Error executing Python script');
        }
        if (stderr) {
          console.error('⚠️ Python script stderr:', stderr);
        }

        try {
          const result = stdout.trim();
          resolve(result);
        } catch (parseError) {
          console.error('❌ Error parsing Python script output:', parseError);
          reject('Error parsing Python script output');
        }
      }
    );
  });
};
