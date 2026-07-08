import { Component, inject } from '@angular/core';
import { Chat } from './services/chat';

@Component({
  selector: 'app-game',
  imports: [],
  templateUrl: './game.html',
  styleUrl: './game.css',
})
export class Game {
  private chatService = inject(Chat);

  public onClickConnect() {
    this.chatService.connect();
  }

  public onClickDisconnect() {
    this.chatService.disconnect();
  }

  public onClickSendMessage() {
    const message = 'Hello from Angular!';
    this.chatService.sendMessage(message);
  }

  public onClickConnectToChatRoom() {
    this.chatService.connectToChatRoom();
  }
}
