export interface ChatRequest {
  question: string;
}

export interface ChatSource {
  source: string;
  page: number | string;
  text: string;
}

export interface ChatResponse {
  answer: string;
  sources: ChatSource[];
}