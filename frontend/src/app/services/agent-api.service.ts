import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { QueryRequest, QueryResponse } from '../models/asset.model';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class AgentApiService {
  private readonly base = environment.agentApiUrl;

  constructor(private http: HttpClient) {}

  query(req: QueryRequest): Observable<QueryResponse> {
    return this.http.post<QueryResponse>(`${this.base}/api/query`, req);
  }
}
