import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { ClaimService } from '../../../../core/services/claim.service';
import { ClaimStatus } from '../../../../core/models/claim.model';

@Component({
  selector: 'app-claim-form',
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './claim-form.component.html',
  styleUrls: ['./claim-form.component.css']
})
export class ClaimFormComponent {
  private readonly fb = inject(FormBuilder);
  private readonly claimService = inject(ClaimService);
  private readonly router = inject(Router);

  submitting = false;
  errorMessage = '';
  statuses = Object.values(ClaimStatus);

  claimForm: FormGroup = this.fb.group({
    title: ['', [Validators.required, Validators.minLength(3)]],
    description: [''],
    status: [ClaimStatus.PENDING, [Validators.required]]
  });

  onSubmit(): void {
    if (this.claimForm.invalid) {
      this.claimForm.markAllAsTouched();
      return;
    }

    this.submitting = true;
    this.errorMessage = '';
    const claimData = this.claimForm.value;

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

  onCancel(): void {
    this.router.navigate(['/claims']);
  }
}
