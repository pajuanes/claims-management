import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Damage, DamageCreate } from '../models/claim.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DamageService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = environment.apiUrl;

  createDamage(claimId: string, damage: DamageCreate): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/claims/${claimId}/damages`, damage);
  }

  updateDamage(claimId: string, damageId: string, damage: Partial<Damage>): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/claims/${claimId}/damages/${damageId}`, damage);
  }

  deleteDamage(claimId: string, damageId: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/claims/${claimId}/damages/${damageId}`);
  }
}
