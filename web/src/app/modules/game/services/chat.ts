import { Injectable } from "@angular/core";
import { Subject } from "rxjs";
import { environment } from "../../../../environments/environment";

@Injectable({
  providedIn: 'root',
})
export class Chat {
  private wsConnection: WebSocket | null = null;

  private onMessageEmitter = new Subject<string>();

  private onOpen = () => {
    console.log('WebSocket connection established.');
  };

  private onMessage = (event: Event) => {
    const messageEvent = event as MessageEvent;
    this.onMessageEmitter.next(messageEvent.data);
    console.log('Received message:', messageEvent.data);
  };

  private onClose = () => {
    console.log('WebSocket connection closed.');
    this.wsConnection = null;
  };

  private onError = (error: Event) => {
    console.error('WebSocket error:', error);
  };

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
}