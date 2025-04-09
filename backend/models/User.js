import mongoose from 'mongoose';

const userSchema = new mongoose.Schema({
  user_id: { type: Number, required: true, unique: true },
  orders: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Order' }],
  id_creation_date: { type: Date, default: Date.now }
});

const User = mongoose.model('User', userSchema);
export default User;
