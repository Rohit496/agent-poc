import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ChatBotComponent } from './components/chat-bot/chat-bot.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, ChatBotComponent],
  template: `
    <router-outlet />
    <app-chat-bot />
  `,
})
export class AppComponent {}
