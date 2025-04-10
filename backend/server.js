import express from "express";
import dotenv from "dotenv";
import cors from "cors";
import cookieParser from "cookie-parser"; // ✅ Add this

import queryRoutes from "./routes/queryRoutes.js";
import connectDB from "./mongodb_connect.js";
import orderRoutes from "./routes/add_details/orderRoutes.js";
import userRoutes from "./routes/add_details/userRoutes.js";
import signupRoutes from "./routes/add_details/signupRoutes.js";
import signinRoutes from "./routes/add_details/signinRoutes.js";

dotenv.config();  // Load environment variables
connectDB();

const app = express();
const PORT = process.env.PORT || 5001; // Use port 5001 as fallback

// ✅ Middlewares
app.use(cors({
  origin: "http://localhost:5173", // adjust to your frontend
  credentials: true,              // ✅ Allow sending cookies
}));
app.use(cookieParser());          // ✅ Enable cookie parsing
app.use(express.json());          // Parse incoming JSON

// ✅ Routes
app.use("/api", signupRoutes);    // Handle user signup at /api/signup
app.use("/api", signinRoutes);    // Handle user signin at /api/signin
app.use("/api", orderRoutes);
app.use("/api", userRoutes);
app.use("/api", queryRoutes);     // /api/query will be protected by auth middleware

// ✅ Start server
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
