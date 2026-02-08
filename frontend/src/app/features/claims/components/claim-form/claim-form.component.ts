import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { ClaimService } from '../../../../core/services/claim.service';
import { ClaimStatus } from '../../../../core/models/claim.model';

@Component({
  selector: 'app-claim-form',
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './claim-form.component.html',
  styleUrls: ['./claim-form.component.css']
})
export class ClaimFormComponent implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly claimService = inject(ClaimService);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);

  submitting = false;
  errorMessage = '';
  statuses = Object.values(ClaimStatus);
  isEditMode = false;
  claimId: string | null = null;

  claimForm: FormGroup = this.fb.group({
    title: ['', [Validators.required, Validators.minLength(3)]],
    description: [''],
    status: [ClaimStatus.PENDING, [Validators.required]]
  });

  ngOnInit(): void {
    this.claimId = this.route.snapshot.paramMap.get('id');
    if (this.claimId) {
      this.isEditMode = true;
      this.loadClaim(this.claimId);
    }
  }

  loadClaim(id: string): void {
    this.claimService.getClaim(id).subscribe({
      next: (claim) => {
        this.claimForm.patchValue({
          title: claim.title,
          description: claim.description,
          status: claim.status
        });
      },
      error: (err) => {
        console.error('Failed to load claim', err);
        this.errorMessage = 'Failed to load claim';
      }
    });
  }

  onSubmit(): void {
    if (this.claimForm.invalid) {
      this.claimForm.markAllAsTouched();
      return;
    }

    this.submitting = true;
    this.errorMessage = '';
    const claimData = this.claimForm.value;

    if (this.isEditMode && this.claimId) {
      this.claimService.updateClaim(this.claimId, claimData).subscribe({
        next: (claim) => {
          this.router.navigate(['/claims', this.claimId]);
        },
        error: (err) => {
          console.error('Failed to update claim', err);
          this.errorMessage = err.error?.detail || 'Failed to update claim. Please try again.';
          this.submitting = false;
        }
      });
    } else {
      this.claimService.createClaim(claimData).subscribe({
        next: (claim) => {
          if (claim && claim.id) {
            this.router.navigate(['/claims', claim.id]);
          } else {
            this.errorMessage = 'Claim created but no ID returned';
            this.submitting = false;
            setTimeout(() => this.router.navigate(['/claims']), 2000);
          }
        },
        error: (err) => {
          console.error('Failed to create claim', err);
          this.errorMessage = err.error?.detail || 'Failed to create claim. Please try again.';
          this.submitting = false;
        }
      });
    }
  }

  onCancel(): void {
    this.router.navigate(['/claims']);
  }
}
