import jwt from "jsonwebtoken";

const authMiddleware = (req, res, next) => {
  let token = null;
  const authHeader = req.headers.authorization;

  // ✅ Try getting token from Authorization header
  if (authHeader && authHeader.startsWith("Bearer ")) {
    token = authHeader.split(" ")[1];
    console.log("📦 Token found in header:", token);
  }

  // ✅ If not in header, try cookies
  if (!token && req.cookies?.token) {
    token = req.cookies.token;
    console.log("🍪 Token found in cookies:", token);
  }

  if (!token) {
    console.log("❌ No token provided in header or cookies");
    return res.status(401).json({ error: "Access denied. No token provided." });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET || "your_jwt_secret");
    req.user = decoded;

    // ✅ Debug decoded token
    console.log("🔓 Token verified. Decoded payload:", decoded);

    next();
  } catch (err) {
    console.log("⚠️ Invalid or expired token:", err.message);
    return res.status(401).json({ error: "Invalid or expired token." });
  }
};

export default authMiddleware;
