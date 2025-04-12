import { Injectable } from '@angular/core';

@Injectable({
    providedIn: 'root',
})
export class StorageService {
    private socket: WebSocket;
    private readonly messageQueue: any[] = [];
    private isSocketOpen = false;

    constructor() {
        this.socket = new WebSocket('ws://localhost:8080');
        

        this.socket.onopen = () => {
            console.log('WebSocket connection established');
            this.isSocketOpen = true;
            this.flushMessageQueue();
        };

        this.socket.onclose = () => {
            console.log('WebSocket connection closed');
            this.isSocketOpen = false;
        };

        this.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
        this.socket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            if (message.type === 'update') {
                console.log('Received update:', message.key, message.value);
            } else if (message.type === 'fetch') {
                console.log('Received fetch:', message.key, message.value);
            }
        };
    }

    private flushMessageQueue(): void {
        while (this.messageQueue.length > 0 && this.isSocketOpen) {
            const message = this.messageQueue.shift();
            this.socket.send(JSON.stringify(message));
        }
    }

    private ensureSocketConnection(callback: () => void): void {
        if (this.isSocketOpen) {
            callback();
        } else {
            const interval = setInterval(() => {
                if (this.isSocketOpen) {
                    clearInterval(interval);
                    callback();
                }
            }, 100);

            // Reopen the socket if it's closed
            if (this.socket.readyState === WebSocket.CLOSED) {
                this.socket = new WebSocket('ws://localhost:8080');
            }
        }
    }

    fetchState(key: string): Promise<any> {
        return new Promise((resolve, reject) => {
            this.ensureSocketConnection(() => {
                this.socket.onmessage = (event) => {
                    console.log('Received message:', event.data);
                    const message = JSON.parse(event.data);
                    if (message.type === 'fetch' && message.key === key) {
                        resolve(message.value);
                    }
                };

                this.socket.send(JSON.stringify({ type: 'fetch', key }));
            });
        });
    }

    updateState(key: string, value: any): void {
        const message = { type: 'update', key, value };
        console.log('Sending update:', message);
        if (this.isSocketOpen) {
            console.log('WebSocket is open. Sending message:', message);
            this.socket.send(JSON.stringify(message));
        } else {
            console.warn('WebSocket is closed. Queueing message for later:', message);
            this.messageQueue.push(message);
            this.ensureSocketConnection(() => this.flushMessageQueue());
        }
    }
}
