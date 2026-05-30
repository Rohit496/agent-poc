import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  ScanRequest,
  ScanResponse,
  ScanPackagesResponse,
  ScanEcosystem,
  ScanProfile,
} from '../models/scan.model';

@Injectable({ providedIn: 'root' })
export class ScanApiService {
  constructor(private http: HttpClient) {}

  triggerScan(req: ScanRequest): Observable<ScanResponse> {
    return this.http.post<ScanResponse>('/api/scan', req);
  }

  scanPackages(req: ScanRequest, limit = 100, ecosystemFilter = ''): Observable<ScanPackagesResponse> {
    const params: Record<string, string> = { limit: String(limit) };
    if (ecosystemFilter) params['ecosystem_filter'] = ecosystemFilter;
    return this.http.post<ScanPackagesResponse>('/api/scan/packages', req, { params });
  }

  scanFindings(req: ScanRequest): Observable<ScanResponse> {
    return this.http.post<ScanResponse>('/api/scan/findings', req);
  }

  getEcosystems(): Observable<{ ecosystems: ScanEcosystem[] }> {
    return this.http.get<{ ecosystems: ScanEcosystem[] }>('/api/scan/ecosystems');
  }

  getProfiles(): Observable<{ profiles: ScanProfile[] }> {
    return this.http.get<{ profiles: ScanProfile[] }>('/api/scan/profiles');
  }
}
