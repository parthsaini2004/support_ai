import express from "express";
import User from "../../models/User.js"; // Add .js

const router = express.Router();

router.post("/adduser", async (req, res) => {
  try {
    const user = new User(req.body);
    const savedUser = await user.save();
    res.status(201).json(savedUser);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

export default router;
