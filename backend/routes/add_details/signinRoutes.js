import express from "express";
import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";
import User from "../../models/User.js";

const router = express.Router();

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

    // 3. Sign JWT token
    const token = jwt.sign(
      { user_id: user.user_id },
      process.env.JWT_SECRET || "your_jwt_secret",
      { expiresIn: "1h" }
    );

    // 4. ✅ Set token in HTTP cookie
    res.cookie("token", token, {
      httpOnly: false,           // if true: not accessible in frontend JS
      secure: false,             // true in production (HTTPS)
      sameSite: "Lax",           // allows sending cookies on same-site navigations
      maxAge: 60 * 60 * 1000,    // 1 hour in milliseconds
    });

    // 5. ✅ Send token also in response (optional)
    res.status(200).json({
      message: "Logged in successfully",
      token,
      user: {
        username: user.username,
        email: user.email,
        user_id: user.user_id,
      },
    });

  } catch (err) {
    console.error("❌ Signin error:", err);
    res.status(500).json({ error: err.message });
  }
});

export default router;
