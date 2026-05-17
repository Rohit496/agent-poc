export interface Asset {
  id: string;
  party_number: string;
  asset_type: 'server' | 'hardware';
  name: string;
  status: 'active' | 'inactive' | 'maintenance';
  location: string;
  manufacturer: string;
  model: string;
  serial_number: string;
  purchase_date: string;
  metadata: Record<string, unknown>;
}

export interface QueryRequest {
  query: string;
}

export interface QueryResponse {
  party_number: string;
  summary: string;
  assets: Asset[];
  metadata: {
    total: number;
    filters_applied: Record<string, string>;
  };
}
