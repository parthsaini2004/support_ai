// routes/add_details/logoutRoutes.js
import express from 'express';
const router = express.Router();

// Logout Route
router.post('/logout', (req, res) => {
  res.clearCookie('token', {
    httpOnly: true,
    secure: false,       // set to true if using HTTPS
    sameSite: 'lax',
    path: '/',           // must match how the cookie was originally set
  });

  res.status(200).json({ message: 'Logged out successfully' });
});


// Default export of the router
export default router;
