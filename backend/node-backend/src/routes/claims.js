import express from "express";
import { body } from "express-validator";

import claimsController from "../controllers/claimsController.js";
import validate from "../middleware/validate.js";

const router = express.Router();

// Validaciones
const createClaimValidation = [
  body('title').notEmpty().withMessage('Title is required'),
  body('status').optional().isIn(['PENDING', 'IN_REVIEW', 'FINALIZED', 'CANCELED']),
];

const updateStatusValidation = [
  body('status').isIn(['PENDING', 'IN_REVIEW', 'FINALIZED', 'CANCELED']).withMessage('Invalid status'),
];

const damageValidation = [
  body('part').notEmpty().withMessage('Part is required'),
  body('severity').isIn(['LOW', 'MEDIUM', 'HIGH']).withMessage('Invalid severity'),
  body('image_url').isURL().withMessage('Valid image URL is required'),
  body('price').isFloat({ min: 0 }).withMessage('Price must be a positive number'),
  body('score').isInt({ min: 1, max: 10 }).withMessage('Score must be between 1 and 10'),
];

// Rutas para claims
router.get('/', claimsController.getAllClaims);
router.get('/:id', claimsController.getClaimById);
router.post('/', createClaimValidation, validate, claimsController.createClaim);
router.patch('/:id/status', updateStatusValidation, validate, claimsController.updateClaimStatus);
router.delete('/:id', claimsController.deleteClaim);

// Rutas para damages
router.post('/:id/damages', damageValidation, validate, claimsController.addDamage);
router.put('/:claimId/damages/:damageId', damageValidation, validate, claimsController.updateDamage);
router.delete('/:claimId/damages/:damageId', claimsController.deleteDamage);

export default router;
