import { Injectable, signal } from '@angular/core';

export type UserRole = 'employee' | 'hr_admin';

export interface LoggedInUser {
  email: string;
  role: UserRole;
  displayName: string;
}

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly currentUserSignal =
    signal<LoggedInUser | null>(null);

  readonly currentUser =
    this.currentUserSignal.asReadonly();

  login(
    email: string,
    password: string,
  ): boolean {
    const normalizedEmail = email
      .trim()
      .toLowerCase();

    if (
      normalizedEmail === 'hr@hexaware.com' &&
      password === 'hr@123'
    ) {
      this.currentUserSignal.set({
        email: normalizedEmail,
        role: 'hr_admin',
        displayName: 'HR Administrator',
      });

      return true;
    }

    if (
      normalizedEmail === 'amit@hexaware.com' &&
      password === 'amit@123'
    ) {
      this.currentUserSignal.set({
        email: normalizedEmail,
        role: 'employee',
        displayName: 'Employee User',
      });

      return true;
    }

    return false;
  }

  logout(): void {
    this.currentUserSignal.set(null);
  }

  isLoggedIn(): boolean {
    return this.currentUserSignal() !== null;
  }

  isHrAdmin(): boolean {
    return this.currentUserSignal()?.role === 'hr_admin';
  }
}