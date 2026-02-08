import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { ClaimService } from '../../../../core/services/claim.service';
import { Claim } from '../../../../core/models/claim.model';

@Component({
    selector: 'app-claims-list',
    imports: [CommonModule, RouterModule],
    templateUrl: './claims-list.component.html',
    styleUrls: ['./claims-list.component.css']
})
export class ClaimsListComponent implements OnInit {
  private readonly claimService = inject(ClaimService);
  private readonly router = inject(Router);
  
  claims = signal<Claim[]>([]);
  loading = signal(false);
  error = signal<string | null>(null);

  ngOnInit(): void {
    this.loadClaims();
  }

  loadClaims(): void {
    this.loading.set(true);
    this.error.set(null);
    
    this.claimService.getClaims().subscribe({
      next: (claims) => {
        this.claims.set(claims);
        this.loading.set(false);
      },
      error: (err) => {
        this.error.set('Failed to load claims');
        this.loading.set(false);
        console.error(err);
      }
    });
  }

  navigateToCreate(): void {
    this.router.navigate(['/claims/create']);
  }

  deleteClaim(claimId: string, event: Event): void {
    event.stopPropagation();
    
    if (!confirm('Are you sure you want to delete this claim?')) return;

    console.log('Deleting claim with ID:', claimId);

    this.claimService.deleteClaim(claimId).subscribe({
      next: () => {
        console.log('Claim deleted successfully');
        this.claims.set(this.claims().filter(c => c.id !== claimId));
      },
      error: (err) => {
        console.error('Failed to delete claim - Full error:', err);
        console.error('Error status:', err.status);
        console.error('Error message:', err.message);
        console.error('Error details:', err.error);
        this.error.set(`Failed to delete claim: ${err.error?.message || err.message}`);
      }
    });
  }
}
