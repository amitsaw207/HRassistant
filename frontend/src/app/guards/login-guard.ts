import { inject } from '@angular/core';
import {
  CanActivateFn,
  Router,
} from '@angular/router';

import { AuthService } from '../services/auth';

export const loginGuard: CanActivateFn = () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (!authService.isLoggedIn()) {
    return true;
  }

  const user = authService.currentUser();

  if (user?.role === 'hr_admin') {
    return router.createUrlTree(['/admin']);
  }

  return router.createUrlTree(['/chat']);
};