import { Claim } from "../models/index.js";
import pythonService from "../services/pythonService.js";

class ClaimsController {
  // GET /claims
  async getAllClaims(req, res) {
    try {
      const claims = await Claim.find().sort({ createdAt: -1 });
      res.json(claims);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }

  // GET /claims/:id
  async getClaimById(req, res) {
    try {
      const claim = await Claim.findById(req.params.id);
      if (!claim) {
        return res.status(404).json({ error: "Claim not found" });
      }
      res.json(claim);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }

  // POST /claims
  async createClaim(req, res) {
    try {
      const claim = new Claim(req.body);
      await claim.save();
      res.status(201).json(claim);
    } catch (error) {
      res.status(400).json({ error: error.message });
    }
  }

  // PATCH /claims/:id/status
  async updateClaimStatus(req, res) {
    try {
      const { id } = req.params;
      const { status } = req.body;

      const claim = await Claim.findById(id);
      if (!claim) {
        return res.status(404).json({ error: "Claim not found" });
      }

      const validation =
        await pythonService.validateClaimStatusChange(
          claim.toJSON(),
          status
        );

      if (!validation.valid) {
        return res
          .status(409)
          .json({ error: validation.message || "Invalid status change" });
      }

      claim.status = status;
      await claim.save();

      res.json(claim);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }

  // POST /claims/:id/damages
  async addDamage(req, res) {
    try {
      const claim = await Claim.findById(req.params.id);
      if (!claim) {
        return res.status(404).json({ error: "Claim not found" });
      }

      if (claim.status !== "PENDING") {
        return res
          .status(409)
          .json({ error: "Damages can only be managed when claim is PENDING" });
      }

      claim.damages.push(req.body);
      await claim.save();

      res.status(201).json(claim);
    } catch (error) {
      res.status(400).json({ error: error.message });
    }
  }

  // PUT /claims/:claimId/damages/:damageId
  async updateDamage(req, res) {
    try {
      const claim = await Claim.findById(req.params.claimId);
      if (!claim) {
        return res.status(404).json({ error: "Claim not found" });
      }

      if (claim.status !== "PENDING") {
        return res
          .status(409)
          .json({ error: "Damages can only be managed when claim is PENDING" });
      }

      const damage = claim.damages.id(req.params.damageId);
      if (!damage) {
        return res.status(404).json({ error: "Damage not found" });
      }

      Object.assign(damage, req.body);
      await claim.save();

      res.json(claim);
    } catch (error) {
      res.status(400).json({ error: error.message });
    }
  }

  // DELETE /claims/:claimId/damages/:damageId
  async deleteDamage(req, res) {
    try {
      const claim = await Claim.findById(req.params.claimId);
      if (!claim) {
        return res.status(404).json({ error: "Claim not found" });
      }

      if (claim.status !== "PENDING") {
        return res
          .status(409)
          .json({ error: "Damages can only be managed when claim is PENDING" });
      }

      const damage = claim.damages.id(req.params.damageId);
      if (!damage) {
        return res.status(404).json({ error: "Damage not found" });
      }

      damage.deleteOne();
      await claim.save();

      res.status(204).send();
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }

  // DELETE /claims/:id
  async deleteClaim(req, res) {
    try {
      const claim = await Claim.findByIdAndDelete(req.params.id);
      if (!claim) {
        return res.status(404).json({ error: "Claim not found" });
      }
      res.status(204).send();
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }
}

export default new ClaimsController();
