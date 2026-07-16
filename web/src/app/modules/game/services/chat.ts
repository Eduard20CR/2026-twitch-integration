import { Injectable } from "@angular/core";
import { Subject } from "rxjs";
import { environment } from "../../../../environments/environment";
import { WsMessage } from "../types/ws-message.inteface";

@Injectable({
  providedIn: 'root',
})
export class Chat {
  private wsConnection: WebSocket | null = null;

  private onMessageEmitter = new Subject<string>();

  // PUBLIC METHODS

  public connect(): void {
    if (this.wsConnection) return;

    this.wsConnection = new WebSocket(`${environment.wsUrl}/api/chat`);

    this.wsConnection.onopen = this.onOpen.bind(this);
    this.wsConnection.onmessage = this.onMessage.bind(this);
    this.wsConnection.onclose = this.onClose.bind(this);
    this.wsConnection.onerror = this.onError.bind(this);
  }

  public disconnect(): void {
    if (!this.wsConnection) return;

    this.wsConnection.close();
    this.wsConnection = null;
  }

  public sendMessage(message: string): void {
    if (!this.wsConnection) {
      console.error('WebSocket connection is not established.');
      return;
    }

    this.wsConnection.send(message);
  }

  public connectToChatRoom(): void {
    if (!this.wsConnection) {
      console.error('WebSocket connection is not established.');
      return;
    }

    const messageJson = this.createMessageJson('connect_to_chat_room', null);

    this.wsConnection.send(messageJson);
  }

  public leaveChatRoom(): void {
    if (!this.wsConnection) {
      console.error('WebSocket connection is not established.');
      return;
    }

    const messageJson = this.createMessageJson('leave_chat_room', null);

    this.wsConnection.send(messageJson);
  }

  // WS EVENT HANDLERS

  private onOpen = () => {
    console.log('WebSocket connection established.');
  };

  private onMessage = (event: Event) => {
    const messageEvent = event as MessageEvent;
    const message: WsMessage = JSON.parse(messageEvent.data);

    console.info(message);

    switch (message.event) {
      case 'ping':
        this.onPingMessage(message.payload);
        break;
      case "info_message":
        this.onMessageEmitter.next(message.payload);
        break;
      default:
        console.warn(`Unhandled WebSocket event: ${message.event}`);
    }
  };

  private onClose = () => {
    console.log('WebSocket connection closed.');
    this.wsConnection = null;
  };

  private onError = (error: Event) => {
    console.error('WebSocket error:', error);
  };

  // HELPER METHODS

  private createMessage(event: string, payload: any): WsMessage {
    return { event, payload };
  }

  private createMessageJson(event: string, payload: any): string {
    const message: WsMessage = this.createMessage(event, payload);
    return JSON.stringify(message);
  }

  // EVENT HANDLERS

  private onPingMessage = (_: string) => {
    this.sendMessage(this.createMessageJson('pong', {}));
  }
}