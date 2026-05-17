import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AssetTableComponent } from '../asset-table/asset-table.component';
import { QueryResponse } from '../../models/asset.model';

@Component({
  selector: 'app-agent-response',
  standalone: true,
  imports: [CommonModule, AssetTableComponent],
  templateUrl: './agent-response.component.html',
  styleUrl: './agent-response.component.scss',
})
export class AgentResponseComponent {
  @Input() response!: QueryResponse;
}
