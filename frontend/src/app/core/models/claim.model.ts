export enum ClaimStatus {
  PENDING = 'PENDING',
  IN_REVIEW = 'IN_REVIEW',
  FINALIZED = 'FINALIZED',
  CANCELED = 'CANCELED'
}

export enum DamageSeverity {
  LOW = 'LOW',
  MEDIUM = 'MEDIUM',
  HIGH = 'HIGH'
}

export interface Damage {
  id: string;
  _id?: string;
  part: string;
  severity: DamageSeverity;
  image_url: string;
  price: number;
  score: number;
  claim_id: string;
}

export interface Claim {
  id: string;
  title: string;
  description?: string;
  status: ClaimStatus;
  damages: Damage[];
  total_amount?: number;
}

export interface ClaimCreate {
  title: string;
  description?: string;
  status?: ClaimStatus;
}

export interface DamageCreate {
  part: string;
  severity: DamageSeverity;
  image_url: string;
  price: number;
  score: number;
}
