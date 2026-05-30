import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { ScanApiService } from '../../services/scan-api.service';
import {
  ScanRequest,
  ScanResponse,
  ScanPackagesResponse,
  ScanPackage,
} from '../../models/scan.model';

@Component({
  selector: 'app-scan',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './scan.component.html',
  styleUrl: './scan.component.scss',
})
export class ScanComponent implements OnInit {
  private scanApi = inject(ScanApiService);

  // Form state
  profile: 'baseline' | 'project' | 'deep' = 'baseline';
  root = '';
  ecosystem = '';
  maxDuration = '60s';

  // Results
  scanResult: ScanResponse | null = null;
  packages: ScanPackage[] = [];
  packagesTotal = 0;
  loading = false;
  error = '';

  // Package table
  searchText = '';
  filterEcosystem = '';
  displayedPackages: ScanPackage[] = [];
  ecosystemOptions: string[] = [];

  // View toggle
  activeTab: 'summary' | 'packages' | 'findings' = 'summary';

  ngOnInit(): void {}

  runScan(): void {
    this.loading = true;
    this.error = '';
    this.scanResult = null;
    this.packages = [];

    const req: ScanRequest = {
      profile: this.profile,
      max_duration: this.maxDuration,
    };
    if ((this.profile === 'project' || this.profile === 'deep') && this.root)
      req.root = this.root;
    if (this.ecosystem) req.ecosystem = this.ecosystem;

    this.scanApi.triggerScan(req).subscribe({
      next: (res) => {
        this.scanResult = res;
        this.loading = false;
        if (res.status === 'error') {
          this.error = res.error;
        } else {
          this.ecosystemOptions = Object.keys(res.ecosystem_counts);
        }
      },
      error: (err) => {
        this.error = err.message || 'Scan failed';
        this.loading = false;
      },
    });
  }

  loadPackages(): void {
    this.activeTab = 'packages';
    if (this.packages.length > 0) {
      this.applyPackageFilters();
      return;
    }

    this.loading = true;
    const req: ScanRequest = {
      profile: this.profile,
      max_duration: this.maxDuration,
    };
    if ((this.profile === 'project' || this.profile === 'deep') && this.root)
      req.root = this.root;
    if (this.ecosystem) req.ecosystem = this.ecosystem;

    this.scanApi.scanPackages(req, 500).subscribe({
      next: (res) => {
        this.packages = res.packages;
        this.packagesTotal = res.total;
        this.applyPackageFilters();
        this.loading = false;
      },
      error: (err) => {
        this.error = err.message || 'Failed to load packages';
        this.loading = false;
      },
    });
  }

  applyPackageFilters(): void {
    let result = [...this.packages];
    if (this.filterEcosystem) {
      result = result.filter((p) => p.ecosystem === this.filterEcosystem);
    }
    if (this.searchText) {
      const q = this.searchText.toLowerCase();
      result = result.filter(
        (p) =>
          p.package_name.toLowerCase().includes(q) ||
          p.version.toLowerCase().includes(q) ||
          p.ecosystem.toLowerCase().includes(q),
      );
    }
    this.displayedPackages = result;
  }

  exportCsv(): void {
    const headers = [
      'Ecosystem',
      'Package',
      'Version',
      'Manager',
      'Confidence',
      'Direct',
      'Source Type',
    ];
    const rows = this.displayedPackages.map((p) => [
      p.ecosystem,
      p.package_name,
      p.version,
      p.package_manager,
      p.confidence,
      String(p.direct_dependency ?? ''),
      p.source_type,
    ]);
    const csv = [headers, ...rows].map((r) => r.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'bumblebee-packages.csv';
    a.click();
    URL.revokeObjectURL(url);
  }

  get ecosystemEntries(): [string, number][] {
    if (!this.scanResult) return [];
    return Object.entries(this.scanResult.ecosystem_counts).sort(
      (a, b) => b[1] - a[1],
    );
  }

  get findingsCount(): number {
    return this.scanResult?.findings_total ?? 0;
  }
}
