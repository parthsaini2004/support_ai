import express from "express";
import Order from "../../models/Order.js";
import User from "../../models/User.js";

const router = express.Router();

router.post("/addorder", async (req, res) => {
  try {
    const { user_id, order_id } = req.body;

    // 1. Check if user exists
    const user = await User.findOne({ user_id });
    if (!user) {
      return res.status(404).json({ error: "User not found" });
    }

    // 2. Check if order_id already exists
    const existingOrder = await Order.findOne({ order_id });
    if (existingOrder) {
      return res.status(400).json({ error: "Order with this order_id already exists" });
    }

    // 3. Create and save the order
    const order = new Order(req.body);
    const savedOrder = await order.save();

    // 4. Push the order's _id to user's orders array
    user.orders.push(savedOrder._id);
    await user.save();

    // 5. Return success response
    res.status(201).json({ order: savedOrder, updatedUser: user });

  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

export default router;
