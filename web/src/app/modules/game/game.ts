import { Component, inject } from '@angular/core';
import { Auth } from '../../core/services/auth';

@Component({
  selector: 'app-game',
  imports: [],
  templateUrl: './game.html',
  styleUrl: './game.css',
})
export class Game {
  private authService = inject(Auth);


  public onClickLogout(): void {
    this.authService.logout();
  }
}
