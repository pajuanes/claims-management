import axios from "axios";

class PythonService {
  constructor() {
    this.baseURL = process.env.PYTHON_API_URL || "http://localhost:8001";
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: 5000,
      headers: {
        "Content-Type": "application/json",
      },
    });
  }

  // Validar reglas de negocio complejas usando Python
  async validateClaimStatusChange(claimData, newStatus) {
    try {
      const response = await this.client.post("/api/v1/validate/status-change", {
        claim: claimData,
        new_status: newStatus,
      });
      return response.data;
    } catch (error) {
      console.error("Python validation error:", error.message);
      return { valid: true }; // Fallback: permitir cambio si Python no responde
    }
  }

  // Calcular métricas complejas usando Python
  async calculateClaimMetrics(claimData) {
    try {
      const response = await this.client.post("/api/v1/calculate/metrics", {
        claim: claimData,
      });
      return response.data;
    } catch (error) {
      console.error("Python calculation error:", error.message);
      return {}; // Fallback: retornar objeto vacío
    }
  }
}

export default new PythonService();
