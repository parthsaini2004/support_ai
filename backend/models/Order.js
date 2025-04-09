import mongoose from 'mongoose';

const daysAgo = (days) => {
  const d = new Date();
  d.setDate(d.getDate() - days);
  return d;
};

const orderSchema = new mongoose.Schema({
  order_id: { type: Number, required: true, unique: true },
  completed: { type: Boolean, default: false },
  status: {
    expected_delivery_date: {
      type: Date,
      default: () => daysAgo(3)
    },
    delivery_date: {
      type: Date,
      default: null
    },
    dispatch_date: {
      type: Date,
      default: () => daysAgo(4)
    }
  },
  user_id: { type: Number, required: true },
  order_date: {
    type: Date,
    default: () => daysAgo(5),
    required: true
  },
  price: {
    type: Number,
    default: 2000
  },
  description: {
    type: String,
    required: true
  },
  refund: {
    refundable: {
      type: Boolean,
      default: true
    },
    refundable_within: {
      type: Date,
      default: function () {
        const d = this.order_date || new Date();
        d.setDate(d.getDate() + 7);
        return d;
      }
    }
  }
});

const Order = mongoose.model('Order', orderSchema);
export default Order;
