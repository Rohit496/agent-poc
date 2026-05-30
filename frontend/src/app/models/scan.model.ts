export interface ScanRequest {
  profile: 'baseline' | 'project' | 'deep';
  root?: string;
  ecosystem?: string;
  findings_only?: boolean;
  max_duration?: string;
}

export interface ScanPackage {
  ecosystem: string;
  package_name: string;
  version: string;
  package_manager: string;
  source_type: string;
  confidence: string;
  direct_dependency: boolean | null;
  install_scope: string;
  project_path: string;
  has_lifecycle_scripts: boolean;
}

export interface ScanFinding {
  ecosystem: string;
  package_name: string;
  version: string;
  catalog_id: string;
  catalog_name: string;
  severity: string;
  matched_version: string;
  source_file: string;
  project_path: string;
}

export interface ScanSummary {
  run_id: string;
  profile: string;
  status: string;
  scan_time: string;
  end_time: string;
  duration_ms: number;
  package_records_emitted: number;
  findings_emitted: number;
  files_considered: number;
  roots: { path: string; kind: string }[];
  endpoint: {
    hostname: string;
    os: string;
    arch: string;
    username: string;
    uid: string;
  };
}

export interface ScanResponse {
  status: string;
  packages_total: number;
  findings_total: number;
  ecosystem_counts: Record<string, number>;
  findings: ScanFinding[];
  summary: ScanSummary | null;
  error: string;
}

export interface ScanPackagesResponse {
  status: string;
  total: number;
  returned: number;
  packages: ScanPackage[];
  error?: string;
}

export interface ScanEcosystem {
  id: string;
  label: string;
  file_types: string[];
}

export interface ScanProfile {
  id: string;
  label: string;
  description: string;
}
