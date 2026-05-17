import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AssetStateService } from '../../services/asset-state.service';
import { AssetTableComponent } from '../../components/asset-table/asset-table.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, AssetTableComponent],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
})
export class DashboardComponent {
  constructor(public assetState: AssetStateService) {}
}
