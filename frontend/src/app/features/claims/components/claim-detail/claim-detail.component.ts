import { Component, OnInit, inject, signal, computed, ViewContainerRef, ComponentRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { ClaimService } from '../../../../core/services/claim.service';
import { DamageService } from '../../../../core/services/damage.service';
import { Claim, Damage } from '../../../../core/models/claim.model';

@Component({
    selector: 'app-claim-detail',
    imports: [CommonModule, RouterModule],
    templateUrl: './claim-detail.component.html',
    styleUrls: ['./claim-detail.component.css']
})
export class ClaimDetailComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly claimService = inject(ClaimService);
  private readonly damageService = inject(DamageService);
  private readonly viewContainerRef = inject(ViewContainerRef);

  claim = signal<Claim | null>(null);
  loading = signal(false);
  showDamageForm = signal(false);
  editingDamage = signal<Damage | null>(null);
  private damageFormRef: ComponentRef<any> | null = null;

  totalAmount = computed(() => {
    const claimData = this.claim();
    if (!claimData) return 0;
    return claimData.damages.reduce((sum, damage) => sum + damage.price, 0);
  });

  canManageDamages = computed(() => {
    return this.claim()?.status === 'PENDING';
  });

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.loadClaim(id);
    }
  }

  async toggleDamageForm(show: boolean, damage?: Damage): Promise<void> {
    if (!show && this.damageFormRef) {
      this.damageFormRef.destroy();
      this.damageFormRef = null;
    }
    
    this.showDamageForm.set(show);
    this.editingDamage.set(damage || null);
    
    if (show) {
      const { DamageFormComponent } = await import('../damage-form/damage-form.component');
      this.damageFormRef = this.viewContainerRef.createComponent(DamageFormComponent);
      
      const claimData = this.claim();
      if (claimData) {
        this.damageFormRef.instance.claimId = claimData.id;
        if (damage) {
          this.damageFormRef.instance.damage = damage;
        }
        this.damageFormRef.instance.damageCreated.subscribe((updatedClaim: any) => this.onDamageCreated(updatedClaim));
        this.damageFormRef.instance.cancelled.subscribe(() => this.toggleDamageForm(false));
      }
    }
  }

  loadClaim(id: string): void {
    this.loading.set(true);
    this.claimService.getClaim(id).subscribe({
      next: (claim) => {
        const normalizedClaim = {
          ...claim,
          damages: claim.damages.map((d: any) => ({
            ...d,
            price: typeof d.price === 'object' ? parseFloat(d.price.$numberDecimal) : d.price
          }))
        };
        this.claim.set(normalizedClaim);
        this.loading.set(false);
      },
      error: (err) => {
        console.error('Failed to load claim', err);
        this.loading.set(false);
      }
    });
  }

  onDamageCreated(updatedClaim: any): void {
    const normalizedClaim = {
      ...updatedClaim,
      damages: updatedClaim.damages.map((d: any) => ({
        ...d,
        price: typeof d.price === 'object' ? parseFloat(d.price.$numberDecimal) : d.price
      }))
    };
    this.claim.set(normalizedClaim);
    this.toggleDamageForm(false);
  }

  deleteDamage(damageId: string): void {
    if (!confirm('Are you sure you want to delete this damage?')) return;

    const currentClaim = this.claim();
    if (!currentClaim) return;

    this.damageService.deleteDamage(currentClaim.id, damageId).subscribe({
      next: () => {
        this.loadClaim(currentClaim.id);
      },
      error: (err) => console.error('Failed to delete damage', err)
    });
  }

  editDamage(damage: Damage): void {
    this.toggleDamageForm(true, damage);
  }
}
