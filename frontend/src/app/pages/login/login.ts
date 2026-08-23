import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.scss',
})
export class Login {
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);

  email = '';
  password = '';
  errorMessage = '';
  loading = false;

  login(): void {
    this.errorMessage = '';

    const email = this.email.trim();

    if (!email || !this.password) {
      this.errorMessage =
        'Please enter your email and password.';
      return;
    }

    this.loading = true;

    const success = this.authService.login(
      email,
      this.password,
    );

    if (!success) {
      this.errorMessage =
        'Invalid email or password.';
      this.loading = false;
      return;
    }

    const user = this.authService.currentUser();

    this.loading = false;

    if (user?.role === 'hr_admin') {
      this.router.navigate(['/admin']);
    } else {
      this.router.navigate(['/chat']);
    }
  }
}