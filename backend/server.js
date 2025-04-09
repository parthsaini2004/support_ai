import express from "express";
import dotenv from "dotenv";
import cors from "cors";
import queryRoutes from "./routes/queryRoutes.js";
import connectDB from "./mongodb_connect.js";
import orderRoutes from "./routes/add_details/orderRoutes.js";
import userRoutes from "./routes/add_details/userRoutes.js";

dotenv.config();  // Load environment variables
connectDB();
const app = express();
const PORT = process.env.PORT || 5001; // Use port 5001 as fallback

app.use(cors()); // Enable CORS for frontend-backend communication
app.use(express.json()); // Parse incoming JSON

// Mount query routes directly at /api (routes/queryRoutes.js will handle /query)

app.use("/api", orderRoutes);
app.use("/api", userRoutes);
app.use("/api", queryRoutes);

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
