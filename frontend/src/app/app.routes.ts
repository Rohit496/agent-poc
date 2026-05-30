import { Routes } from '@angular/router';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { ScanComponent } from './pages/scan/scan.component';

export const routes: Routes = [
  { path: '', component: DashboardComponent },
  { path: 'scan', component: ScanComponent },
  { path: '**', redirectTo: '' },
];
