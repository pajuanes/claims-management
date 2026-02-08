import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Claim, ClaimCreate } from '../models/claim.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ClaimService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = `${environment.apiUrl}/claims`;

  getClaims(): Observable<Claim[]> {
    return this.http.get<Claim[]>(this.apiUrl);
  }

  getClaim(id: string): Observable<Claim> {
    return this.http.get<Claim>(`${this.apiUrl}/${id}`);
  }

  createClaim(claim: ClaimCreate): Observable<Claim> {
    return this.http.post<Claim>(this.apiUrl, claim);
  }

  updateClaim(id: string, claim: Partial<Claim>): Observable<Claim> {
    return this.http.put<Claim>(`${this.apiUrl}/${id}`, claim);
  }

  deleteClaim(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
}
