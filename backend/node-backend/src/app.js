import dotenv from "dotenv";
dotenv.config({ path: new URL("../.env.common", import.meta.url).pathname });
dotenv.config();

import express from "express";
import cors from "cors";
import helmet from "helmet";

import { connectDB } from "./config/database.js";
import claimsRoutes from "./routes/claims.js";

const app = express();
const PORT = process.env.PORT || 3000;

// Conectar a MongoDB
connectDB().catch(err => {
  console.error("Mongo connection error:", err.message);
});

// Middleware
app.use(helmet());
app.use(cors({
  origin: process.env.FRONTEND_URL || "http://localhost:4200",
  credentials: true
}));
app.use(express.json());

// Rutas
app.use("/api/v1/claims", claimsRoutes);

// Health check
app.get("/health", (_, res) => {
  res.json({ status: "healthy", service: "node-backend" });
});

// 404 handler
app.use("*", (_, res) => {
  res.status(404).json({ error: "Route not found" });
});

// Error handler
app.use((err, _req, res, _next) => {
  console.error(err.stack);
  res.status(500).json({ error: "Something went wrong!" });
});

app.listen(PORT, () => {
  console.log(`Node.js server running on port ${PORT}`);
});

export default app;
