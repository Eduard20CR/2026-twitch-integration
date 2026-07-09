import { Component, inject, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Auth } from '../../services/auth';

@Component({
  selector: 'app-navbar',
  imports: [RouterLink],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class Navbar implements OnInit {
  private authService = inject(Auth);

  public userInformation = this.authService.userInformation$;

  public onClickLogout(): void {
    this.authService.logout();
  }

  ngOnInit(): void {
    this.authService.getMe();
  }
}
