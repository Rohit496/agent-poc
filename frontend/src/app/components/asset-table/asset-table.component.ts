import { Component, Input, OnChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Asset } from '../../models/asset.model';

type SortDir = 'asc' | 'desc';
type SortKey = keyof Pick<Asset, 'name' | 'asset_type' | 'status' | 'location' | 'manufacturer' | 'purchase_date'>;

@Component({
  selector: 'app-asset-table',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './asset-table.component.html',
  styleUrl: './asset-table.component.scss',
})
export class AssetTableComponent implements OnChanges {
  @Input() assets: Asset[] = [];

  filterType = '';
  filterStatus = '';
  searchText = '';
  sortKey: SortKey = 'name';
  sortDir: SortDir = 'asc';

  displayed: Asset[] = [];

  ngOnChanges(): void {
    this.apply();
  }

  apply(): void {
    let result = [...this.assets];

    if (this.filterType) result = result.filter(a => a.asset_type === this.filterType);
    if (this.filterStatus) result = result.filter(a => a.status === this.filterStatus);
    if (this.searchText) {
      const q = this.searchText.toLowerCase();
      result = result.filter(a =>
        a.name.toLowerCase().includes(q) ||
        a.model.toLowerCase().includes(q) ||
        a.location.toLowerCase().includes(q) ||
        a.manufacturer.toLowerCase().includes(q)
      );
    }

    result.sort((a, b) => {
      const av = a[this.sortKey] ?? '';
      const bv = b[this.sortKey] ?? '';
      return this.sortDir === 'asc'
        ? String(av).localeCompare(String(bv))
        : String(bv).localeCompare(String(av));
    });

    this.displayed = result;
  }

  sort(key: SortKey): void {
    if (this.sortKey === key) {
      this.sortDir = this.sortDir === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortKey = key;
      this.sortDir = 'asc';
    }
    this.apply();
  }

  exportCsv(): void {
    const headers = ['ID', 'Name', 'Type', 'Status', 'Location', 'Manufacturer', 'Model', 'Serial', 'Purchase Date'];
    const rows = this.displayed.map(a => [
      a.id, a.name, a.asset_type, a.status, a.location, a.manufacturer, a.model, a.serial_number, a.purchase_date,
    ]);
    const csv = [headers, ...rows].map(r => r.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `assets-export.csv`;
    a.click();
    URL.revokeObjectURL(url);
  }
}
