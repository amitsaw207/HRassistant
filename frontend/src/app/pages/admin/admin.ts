import {
  Component,
  OnInit,
  inject,
  signal,
} from '@angular/core';
import { DatePipe } from '@angular/common';

import { ApiService } from '../../services/api';
import { DocumentSummary } from '../../models/document';

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [DatePipe],
  templateUrl: './admin.html',
  styleUrl: './admin.scss',
})
export class Admin implements OnInit {
  private readonly apiService = inject(ApiService);

  selectedFile: File | null = null;
  replacementFile: File | null = null;

  documents = signal<DocumentSummary[]>([]);
  selectedDocument = signal<DocumentSummary | null>(null);
  message = signal('');
  errorMessage = signal('');
  loading = signal(false);

  ngOnInit(): void {
    console.log('[ADMIN] Loading documents');
    this.loadDocuments();
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;

    this.selectedFile = input.files?.[0] ?? null;

    console.log(
      '[ADMIN] Selected file:',
      this.selectedFile?.name,
    );

    this.message.set('');
    this.errorMessage.set('');
  }

  onReplacementFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;

    this.replacementFile = input.files?.[0] ?? null;

    console.log(
      '[ADMIN] Replacement file selected:',
      this.replacementFile?.name,
    );
  }

  selectDocumentForUpdate(
    document: DocumentSummary,
  ): void {
    console.log(
      '[ADMIN] Document selected for update:',
      document.filename,
    );

    this.selectedDocument.set(document);
    this.replacementFile = null;
    this.message.set('');
    this.errorMessage.set('');
  }

  clearSelectedDocument(): void {
    this.selectedDocument.set(null);
    this.replacementFile = null;
    this.message.set('');
  }

  uploadDocument(): void {
    if (!this.selectedFile || this.loading()) {
      return;
    }

    const file = this.selectedFile;

    console.log('[ADMIN] Uploading:', file.name);

    this.loading.set(true);
    this.message.set('');
    this.errorMessage.set('');

    this.apiService.uploadDocument(file).subscribe({
      next: (response) => {
        console.log('[ADMIN] Upload response:', response);

        this.message.set(
          `${response.filename} uploaded successfully. ` +
          `${response.chunks_indexed} chunks indexed.`,
        );

        this.selectedFile = null;
        this.loading.set(false);

        this.loadDocuments();
      },

      error: (error) => {
        console.error('[ADMIN] Upload failed:', error);

        this.errorMessage.set(
          'Document upload failed.',
        );

        this.loading.set(false);
      },
    });
  }

  updateDocument(): void {
    const document = this.selectedDocument();
    const file = this.replacementFile;

    if (!document || !file) {
      return;
    }

    console.log(
      '[ADMIN] Updating:',
      document.filename,
      'with',
      file.name,
    );

    this.loading.set(true);
    this.message.set('');
    this.errorMessage.set('');

    this.apiService
      .updateDocument(document.filename, file)
      .subscribe({
        next: (response) => {
          console.log(
            '[ADMIN] Update response:',
            response,
          );

          this.message.set(
            `${response.filename} updated successfully. ` +
            `${response.chunks_indexed} chunks re-indexed.`,
          );

          this.selectedDocument.set(null);
          this.replacementFile = null;
          this.loading.set(false);

          this.loadDocuments();
        },

        error: (error) => {
          console.error(
            '[ADMIN] Update failed:',
            error,
          );

          this.errorMessage.set(
            'Document update failed.',
          );

          this.loading.set(false);
        },
      });
  }

  loadDocuments(): void {
    console.log('[ADMIN] Requesting document list');

    this.apiService.listDocuments().subscribe({
      next: (response) => {
        console.log(
          '[ADMIN] Documents received:',
          response.documents,
        );

        this.documents.set(response.documents);
      },

      error: (error) => {
        console.error(
          '[ADMIN] Document list failed:',
          error,
        );

        this.errorMessage.set(
          'Unable to load the document list.',
        );
      },
    });
  }
}