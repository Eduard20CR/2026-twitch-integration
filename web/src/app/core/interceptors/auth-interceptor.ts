import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { catchError, switchMap, throwError } from 'rxjs';
import { Auth } from '../services/auth';

let isRefreshing = false;

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const http = inject(HttpClient);
  const authService = inject(Auth);

  if (req.url.includes('/auth/refresh') || req.url.includes('/auth/logout')) {
    return next(req);
  }

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {

      if (error.status !== 401) {
        return throwError(() => error);
      }

      if (isRefreshing) {
        return throwError(() => new Error('Refresh already in progress'));
      }

      isRefreshing = true;

      return authService.refreshToken().pipe(
        switchMap(() => {
          isRefreshing = false;

          return next(req);
        }),
        catchError((refreshError) => {
          isRefreshing = false;

          authService.logout();
          return throwError(() => refreshError);
        })
      );
    })
  );
};