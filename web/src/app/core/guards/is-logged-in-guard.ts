import { HttpClient } from '@angular/common/http';
import { inject } from '@angular/core';
import { CanActivateFn } from '@angular/router';
import { catchError, map, of } from 'rxjs';
import { environment } from '../../../environments/environment';

export const isLoggedInGuard: CanActivateFn = (route, state) => {
  const httpClient = inject(HttpClient);

  return httpClient.get(`${environment.backendUrl}/api/auth/check`, { withCredentials: true }).pipe(
    map(() => {
      console.log("Logged");

      return true;
    }),
    catchError(() => {
      console.log("Error");

      window.location.href = `${environment.backendUrl}/api/auth/login`;
      return of(false);
    })
  );

};
