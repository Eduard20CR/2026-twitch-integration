import { Component, inject, OnInit, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Auth } from './core/services/auth';
import { Navbar } from './core/layout/navbar/navbar';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Navbar],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  private authService = inject(Auth);

  protected readonly title = signal('app');

  ngOnInit(): void {
    // this.authService.refreshToken();
  }
}
