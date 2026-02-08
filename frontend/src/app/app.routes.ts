import { Routes } from '@angular/router';
import { ClaimsListComponent } from './features/claims/components/claims-list/claims-list.component';
import { ClaimDetailComponent } from './features/claims/components/claim-detail/claim-detail.component';
import { ClaimFormComponent } from './features/claims/components/claim-form/claim-form.component';

export const routes: Routes = [
  { path: '', redirectTo: '/claims', pathMatch: 'full' },
  { path: 'claims', component: ClaimsListComponent },
  { path: 'claims/create', component: ClaimFormComponent },
  { path: 'claims/edit/:id', component: ClaimFormComponent },
  { path: 'claims/:id', component: ClaimDetailComponent },
  { path: '**', redirectTo: '/claims' }
];
