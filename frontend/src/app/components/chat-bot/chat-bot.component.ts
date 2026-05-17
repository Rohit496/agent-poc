import { Component, signal, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { AgentApiService } from '../../services/agent-api.service';
import { AssetStateService } from '../../services/asset-state.service';
import { FormatMessagePipe } from '../../pipes/format-message.pipe';

interface ChatMessage {
  role: 'user' | 'agent';
  text: string;
  loading?: boolean;
}

@Component({
  selector: 'app-chat-bot',
  standalone: true,
  imports: [CommonModule, FormsModule, FormatMessagePipe],
  templateUrl: './chat-bot.component.html',
  styleUrl: './chat-bot.component.scss',
})
export class ChatBotComponent implements AfterViewChecked {
  @ViewChild('messagesEnd') messagesEnd!: ElementRef;

  private audioContext?: AudioContext;

  isOpen = signal(false);
  inputText = '';
  loading = signal(false);
  messages = signal<ChatMessage[]>([
    {
      role: 'agent',
      text: "Hi! I'm your asset intelligence assistant. Just ask me anything — include a Party Number like P-10042 in your message and I'll find the assets for you.",
    },
  ]);

  readonly suggestions = [
    'Show me all active servers for P-10042',
    'List all hardware in DC-East for P-20017',
    'Which servers are in maintenance for P-30099?',
    'Show all assets for P-20017',
  ];

  get showSuggestions(): boolean {
    return this.messages().length === 1 && !this.loading();
  }

  constructor(
    private agentApi: AgentApiService,
    private assetState: AssetStateService
  ) {}

  ngAfterViewChecked(): void {
    this.scrollToBottom();
  }

  toggle(): void {
    this.isOpen.update(v => !v);
  }

  get canSend(): boolean {
    return this.inputText.trim().length >= 3 && !this.loading();
  }

  send(): void {
    if (!this.canSend) return;

    const userText = this.inputText.trim();
    this.inputText = '';

    this.messages.update(msgs => [...msgs, { role: 'user', text: userText }]);
    this.messages.update(msgs => [...msgs, { role: 'agent', text: '', loading: true }]);
    this.loading.set(true);
    this.primeCompletionTone();

    this.agentApi.query({ query: userText }).subscribe({
      next: (res) => {
        this.assetState.setResponse(res.party_number, res);
        const count = res.assets.length;
        const dashboardNote = count > 0
          ? `\n\nFound **${count}** asset${count !== 1 ? 's' : ''} — dashboard updated.`
          : '';
        this.messages.update(msgs => [
          ...msgs.slice(0, -1),
          { role: 'agent', text: res.summary + dashboardNote },
        ]);
        this.loading.set(false);
        this.playCompletionTone();
      },
      error: (err: HttpErrorResponse) => {
        const msg = err.error?.detail ?? 'Something went wrong. Please try again.';
        this.messages.update(msgs => [
          ...msgs.slice(0, -1),
          { role: 'agent', text: `Error: ${msg}` },
        ]);
        this.loading.set(false);
      },
    });
  }

  useSuggestion(text: string): void {
    this.inputText = text;
    this.send();
  }

  onKeydown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.send();
    }
  }

  private scrollToBottom(): void {
    try {
      this.messagesEnd?.nativeElement?.scrollIntoView({ behavior: 'smooth' });
    } catch {}
  }

  private primeCompletionTone(): void {
    try {
      this.getAudioContext()?.resume();
    } catch {}
  }

  private playCompletionTone(): void {
    const context = this.getAudioContext();
    if (!context) return;

    const play = (): void => {
      const notes = [
        { frequency: 659.25, start: 0, duration: 0.08 },
        { frequency: 880, start: 0.09, duration: 0.12 },
      ];

      for (const note of notes) {
        const oscillator = context.createOscillator();
        const gain = context.createGain();
        const startsAt = context.currentTime + note.start;
        const endsAt = startsAt + note.duration;

        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(note.frequency, startsAt);
        gain.gain.setValueAtTime(0.0001, startsAt);
        gain.gain.exponentialRampToValueAtTime(0.08, startsAt + 0.015);
        gain.gain.exponentialRampToValueAtTime(0.0001, endsAt);

        oscillator.connect(gain);
        gain.connect(context.destination);
        oscillator.start(startsAt);
        oscillator.stop(endsAt);
      }
    };

    if (context.state === 'suspended') {
      context.resume().then(play).catch(() => undefined);
      return;
    }

    play();
  }

  private getAudioContext(): AudioContext | undefined {
    if (this.audioContext) return this.audioContext;

    const AudioContextCtor =
      window.AudioContext ||
      (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;

    if (!AudioContextCtor) return undefined;

    this.audioContext = new AudioContextCtor();
    return this.audioContext;
  }
}
