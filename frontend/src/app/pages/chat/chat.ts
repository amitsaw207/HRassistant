import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { ApiService } from '../../services/api';

interface ChatSource {
  source: string;
  page: number | string;
  text: string;
}

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './chat.html',
  styleUrl: './chat.scss',
})
export class Chat {
  private readonly apiService = inject(ApiService);

  question = '';

  answer = signal('');
  loading = signal(false);
  errorMessage = signal('');
  sources = signal<ChatSource[]>([]);

  askQuestion(): void {
    const value = this.question.trim();

    if (!value || this.loading()) {
      return;
    }

    this.loading.set(true);
    this.answer.set('');
    this.sources.set([]);
    this.errorMessage.set('');

    this.apiService.askQuestion(value).subscribe({
      next: (response) => {
        this.answer.set(response.answer ?? '');
        this.sources.set(response.sources ?? []);
        this.loading.set(false);
      },
      error: (error) => {
        console.error('[CHAT] Error:', error);
        this.errorMessage.set(
          'Unable to process your question.',
        );
        this.loading.set(false);
      },
    });
  }
}