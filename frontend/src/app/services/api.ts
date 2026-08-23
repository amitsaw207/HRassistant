import { Injectable, inject } from '@angular/core';
import {
  HttpClient,
  HttpErrorResponse,
} from '@angular/common/http';
import { Observable, tap, catchError, throwError } from 'rxjs';

import {
  ChatResponse,
} from '../models/chat';

import {
  DocumentListResponse,
  DocumentUploadResponse,
} from '../models/document';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private readonly http = inject(HttpClient);

  private readonly baseUrl =
    'http://127.0.0.1:8000/api';

  askQuestion(question: string): Observable<ChatResponse> {
    const url = `${this.baseUrl}/chat`;

    console.log('[API] Sending chat request:', {
      url,
      question,
    });

    return this.http
      .post<ChatResponse>(url, { question })
      .pipe(
        tap((response) => {
          console.log('[API] Chat response received:', response);
        }),
        catchError((error: HttpErrorResponse) => {
          console.error(
            '[API] Chat request failed:',
            {
              status: error.status,
              message: error.message,
              error: error.error,
            },
          );

          return throwError(() => error);
        }),
      );
  }

  uploadDocument(
    file: File,
  ): Observable<DocumentUploadResponse> {
    const url = `${this.baseUrl}/documents/upload`;
    const formData = new FormData();

    formData.append('file', file);

    console.log('[API] Sending upload request:', {
      url,
      filename: file.name,
      size: file.size,
      type: file.type,
    });

    return this.http
      .post<DocumentUploadResponse>(url, formData)
      .pipe(
        tap((response) => {
          console.log(
            '[API] Upload response received:',
            response,
          );
        }),
        catchError((error: HttpErrorResponse) => {
          console.error(
            '[API] Upload request failed:',
            {
              status: error.status,
              message: error.message,
              error: error.error,
            },
          );

          return throwError(() => error);
        }),
      );
  }

  updateDocument(
  filename: string,
  file: File,
): Observable<DocumentUploadResponse> {
  const url = `${this.baseUrl}/documents/${encodeURIComponent(filename)}`;
  const formData = new FormData();

  formData.append('file', file);

  console.log('[API] Sending update request:', {
    url,
    filename,
    replacementFile: file.name,
  });

  return this.http
    .put<DocumentUploadResponse>(url, formData)
    .pipe(
      tap((response) => {
        console.log(
          '[API] Update response received:',
          response,
        );
      }),
      catchError((error: HttpErrorResponse) => {
        console.error(
          '[API] Update request failed:',
          {
            status: error.status,
            message: error.message,
            error: error.error,
          },
        );

        return throwError(() => error);
      }),
    );
}

  listDocuments(): Observable<DocumentListResponse> {
    const url = `${this.baseUrl}/documents`;

    console.log('[API] Sending document list request:', url);

    return this.http
      .get<DocumentListResponse>(url)
      .pipe(
        tap((response) => {
          console.log(
            '[API] Document list response:',
            response,
          );
        }),
        catchError((error: HttpErrorResponse) => {
          console.error(
            '[API] Document list request failed:',
            {
              status: error.status,
              message: error.message,
              error: error.error,
            },
          );

          return throwError(() => error);
        }),
      );
  }
}