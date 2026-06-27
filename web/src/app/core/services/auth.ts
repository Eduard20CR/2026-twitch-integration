import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class Auth {
  private httpClient = inject(HttpClient);

  public getMe() {
    this.httpClient.get('http://localhost:8000/api/auth/me', { withCredentials: true }).subscribe((response) => {
      console.log('response', response)
    })
  }

  public refreshToken() {
    this.httpClient.get('http://localhost:8000/api/auth/refresh', { withCredentials: true }).subscribe((response) => {
      console.log('response', response)
    })
  }
}
