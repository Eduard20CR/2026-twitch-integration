import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class Auth {
  private httpClient = inject(HttpClient);
  private router = inject(Router);

  public getMe() {
    this.httpClient.get('http://localhost:8000/api/auth/me').subscribe((response) => {
      console.log('response', response)
    })
  }

  public refreshToken(): Observable<any> {
    return this.httpClient.get('http://localhost:8000/api/auth/refresh')
  }

  public logout() {
    return this.httpClient.post('http://localhost:8000/api/auth/logout', {}).subscribe((response) => {
      this.router.navigate(['/'])
    })
  }
}
