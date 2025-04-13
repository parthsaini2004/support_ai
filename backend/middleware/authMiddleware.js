import jwt from 'jsonwebtoken';
import User from '../models/User.js';

/**
 * Middleware to protect routes requiring authentication
 * Verifies JWT token and attaches user to request object
 */
export const protect = async (req, res, next) => {
  let token = null;

  try {
    // Check for token in Authorization header
    if (
      req.headers.authorization &&
      req.headers.authorization.startsWith('Bearer ')
    ) {
      token = req.headers.authorization.split(' ')[1];
    }
    // Fallback to token in cookies
    else if (req.cookies?.token) {
      token = req.cookies.token;
    }

    if (!token) {
      return res.status(401).json({
        success: false,
        error: 'Not authorized, no token provided',
      });
    }

    // Decode and verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);

    // Fetch user from DB and attach to request
    const user = await User.findOne({ user_id: decoded.user_id }).select('-password');

    if (!user) {
      return res.status(404).json({
        success: false,
        error: 'User not found',
      });
    }

    req.user = user;
    next();
  } catch (error) {
    console.error('Authentication error:', error.message);
    return res.status(401).json({
      success: false,
      error: 'Not authorized, token invalid',
    });
  }
};

/**
 * Middleware to check if user is an admin
 */
export const admin = (req, res, next) => {
  if (req.user?.isAdmin) {
    return next();
  } else {
    return res.status(403).json({
      success: false,
      error: 'Not authorized as an admin',
    });
  }
};
