import { createApplication } from '@angular/platform-browser';
import { createCustomElement } from '@angular/elements';
import { ChatBotComponent } from './app/chatbot.component';

(async () => {
  const app = await createApplication();
  const ChatElement = createCustomElement(ChatBotComponent, { injector: app.injector });
  customElements.define('agentrix-chat', ChatElement);
})();
