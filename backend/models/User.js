import mongoose from 'mongoose';
import bcrypt from 'bcryptjs';

// User Schema
const userSchema = new mongoose.Schema({
  user_id: {
    type: Number,
    unique: true
  },
  username: {
    type: String,
    required: true,
    unique: true
  },
  email: {
    type: String,
    required: true,
    unique: true
  },
  password: {
    type: String,
    required: true
  },
  order_ids: [{
    type: Number,
    ref: 'Order'
  }],
  id_creation_date: {
    type: Date,
    default: Date.now
  }
});

// ✅ Merged pre-save hook
userSchema.pre('save', async function (next) {
  try {
    // Assign user_id only for new users
    if (this.isNew) {
      const lastUser = await mongoose.model('User').findOne().sort({ user_id: -1 });
      this.user_id = lastUser ? lastUser.user_id + 1 : 101;
    }

    // Hash password if modified
    if (this.isModified('password')) {
      const salt = await bcrypt.genSalt(10);
      this.password = await bcrypt.hash(this.password, salt);
    }

    next();
  } catch (err) {
    next(err);
  }
});

const User = mongoose.model('User', userSchema);

export default User;
