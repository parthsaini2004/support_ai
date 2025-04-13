import express from "express";
import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";
import User from "../../models/User.js";

const router = express.Router();

// Sign-in route
router.post("/signin", async (req, res) => {
  const { email, password } = req.body;

  console.log("✅ Received signin request:", req.body);

  // 0. Basic validation
  if (!email || !password) {
    return res.status(400).json({ error: "Email and password are required" });
  }

  try {
    // 1. Find user by email
    const user = await User.findOne({ email });
    if (!user) {
      return res.status(404).json({ error: "User not found" });
    }

    // 2. Check password
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return res.status(400).json({ error: "Invalid credentials" });
    }

    // 3. Sign JWT token (store user_id in the token)
    const token = jwt.sign(
      { user_id: user.user_id },   // Include user_id in the JWT payload
      process.env.JWT_SECRET || "your_jwt_secret",   // Make sure to set this in your env file
      { expiresIn: "1h" }  // Token expiration set to 1 hour
    );

    // 4. Set the token in an HTTP cookie
    res.cookie("token", token, {
      httpOnly: true,           // Prevent access to the cookie via JS (for security)
      secure: process.env.NODE_ENV === "production", // Use true in production (HTTPS)
      sameSite: "Lax",          // Allows sending cookies on same-site navigations
      maxAge: 60 * 60 * 1000,   // Token expiration: 1 hour
    });

    // 5. Set user_id in response headers
    res.setHeader("x-user-id", user.user_id);

    // 6. Send token and user data in response (optional)
    res.status(200).json({
      message: "Logged in successfully",
      token,
      user: {
        username: user.username,
        email: user.email,
        user_id: user.user_id,  // Include the user_id here
      },
    });

  } catch (err) {
    console.error("❌ Signin error:", err);
    res.status(500).json({ error: err.message });
  }
});

export default router;
