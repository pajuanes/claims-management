import mongoose from "mongoose";

const DamageSchema = new mongoose.Schema(
  {
    part: { type: String, required: true },
    severity: {
      type: String,
      enum: ["LOW", "MEDIUM", "HIGH"],
      required: true,
    },
    image_url: { type: String, required: true },
    price: {
      type: mongoose.Schema.Types.Decimal128,
      required: true,
      min: 0,
    },
    score: {
      type: Number,
      required: true,
      min: 1,
      max: 10,
    },
  },
  { timestamps: true }
);

const ClaimSchema = new mongoose.Schema(
  {
    title: { type: String, required: true },
    description: { type: String },
    status: {
      type: String,
      enum: ["PENDING", "IN_REVIEW", "FINALIZED", "CANCELED"],
      default: "PENDING",
    },
    damages: [DamageSchema],
  },
  { timestamps: true }
);

// Virtual para calcular total amount
ClaimSchema.virtual("total_amount").get(function () {
  return this.damages.reduce((total, damage) => {
    return total + parseFloat(damage.price.toString());
  }, 0);
});

ClaimSchema.set("toJSON", { virtuals: true });

export const Claim = mongoose.model("Claim", ClaimSchema);
export const Damage = DamageSchema;
