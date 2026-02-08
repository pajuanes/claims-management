import { Component, OnInit, EventEmitter, Input, Output, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { DamageService } from '../../../../core/services/damage.service';
import { Damage, DamageSeverity } from '../../../../core/models/claim.model';

@Component({
    selector: 'app-damage-form',
    imports: [CommonModule, ReactiveFormsModule],
    templateUrl: './damage-form.component.html',
    styleUrls: ['./damage-form.component.css']
})
export class DamageFormComponent implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly damageService = inject(DamageService);

  @Input() claimId!: string;
  @Input() damage?: Damage;
  @Output() damageCreated = new EventEmitter<any>();
  @Output() cancelled = new EventEmitter<void>();

  submitting = false;

  damageForm: FormGroup = this.fb.group({
    part: ['', [Validators.required]],
    severity: ['', [Validators.required]],
    image_url: ['', [Validators.required, Validators.pattern(/^https?:\/\/.+/)]],
    price: [0, [Validators.required, Validators.min(0)]],
    score: [5, [Validators.required, Validators.min(1), Validators.max(10)]]
  });

  ngOnInit(): void {
    if (this.damage) {
      this.damageForm.patchValue(this.damage);
    }
  }

  onSubmit(): void {
    if (this.damageForm.invalid) {
      this.damageForm.markAllAsTouched();
      return;
    }

    this.submitting = true;
    const damageData = this.damageForm.value;

    const request = this.damage
      ? this.damageService.updateDamage(this.claimId, this.damage._id || this.damage.id, damageData)
      : this.damageService.createDamage(this.claimId, damageData);

    request.subscribe({
      next: (response) => {
        this.damageCreated.emit(response);
        this.damageForm.reset();
        this.submitting = false;
      },
      error: (err) => {
        alert(`Failed to ${this.damage ? 'update' : 'create'} damage: ${err.error?.error || err.message}`);
        this.submitting = false;
      }
    });
  }

  onCancel(): void {
    this.cancelled.emit();
  }
}
