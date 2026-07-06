import { HttpClient } from '@angular/common/http';
import { inject, Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { UserInfo } from '../types/me-information.interface';

@Injectable({
  providedIn: 'root',
})
export class Auth {
  private httpClient = inject(HttpClient);
  private router = inject(Router);

  private userInformation = signal<UserInfo | null>(null);
  public userInformation$ = this.userInformation.asReadonly();

  public getMe() {
    this.httpClient.get<UserInfo>('http://localhost:8000/api/auth/me').subscribe({
      next: (response) => {
        this.userInformation.set(response);
      },
      error: (error) => {
        console.error('Error fetching user information:', error);
      },
    })
  }

  public refreshToken(): Observable<any> {
    return this.httpClient.get('http://localhost:8000/api/auth/refresh')
  }

  public logout() {
    return this.httpClient.post('http://localhost:8000/api/auth/logout', {}).subscribe((response) => {
      this.router.navigate(['/'])
      this.userInformation.set(null);
    })
  }
}
