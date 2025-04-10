import express from "express";
import bcrypt from "bcryptjs";
import User from "../../models/User.js";  // Make sure to add .js for ES modules

const router = express.Router();

router.post("/adduser", async (req, res) => {
  try {
    const { username, email, password } = req.body;

    // Check if the user already exists
    const userExists = await User.findOne({ email });
    if (userExists) {
      return res.status(400).json({ error: "User already exists" });
    }

    // Hash the password before saving the user
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);

    // Create a new user object with the hashed password
    const user = new User({
      username,
      email,
      password: hashedPassword,  // Do not pass user_id, it will be auto-generated
    });

    // Save the user to the database
    const savedUser = await user.save();

    res.status(201).json(savedUser);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

export default router;
