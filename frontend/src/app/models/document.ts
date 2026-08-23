export interface DocumentUploadResponse {
  filename: string;
  chunks_indexed: number;
  message: string;
}

export interface DocumentSummary {
  filename: string;
  file_type: string;
  size_kb: number;
  updated_at: string;
  status: string;
}

export interface DocumentListResponse {
  documents: DocumentSummary[];
}