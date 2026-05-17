import { Injectable, signal } from '@angular/core';
import { QueryResponse } from '../models/asset.model';

@Injectable({ providedIn: 'root' })
export class AssetStateService {
  currentResponse = signal<QueryResponse | null>(null);
  currentPartyNumber = signal<string>('');

  setResponse(partyNumber: string, response: QueryResponse): void {
    this.currentPartyNumber.set(partyNumber);
    this.currentResponse.set(response);
  }
}
