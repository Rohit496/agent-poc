import {
  Component,
  Input,
  ElementRef,
  signal,
  ViewChild,
  AfterViewChecked,
} from '@angular/core';
import { FormsModule } from '@angular/forms';
import { FormatMessagePipe } from './format-message.pipe';

interface ChatMessage {
  role: 'user' | 'agent';
  text: string;
  loading?: boolean;
}

interface ToneNote {
  frequency: number;
  start: number;
  duration: number;
  volume: number;
}

@Component({
  selector: 'agentrix-chat-inner',
  standalone: true,
  imports: [FormsModule, FormatMessagePipe],
  templateUrl: './chatbot.component.html',
  styleUrl: './chatbot.component.scss',
})
export class ChatBotComponent implements AfterViewChecked {
  // ── Network ───────────────────────────────────────────────────────────────
  /** Base URL of the backend. Empty = same origin. */
  @Input() apiUrl = '';
  /** API path to POST to. */
  @Input() endpoint = '/api/query';
  /** Request body field name that carries the user query. */
  @Input() queryKey = 'query';
  /**
   * Dot-notation path into the JSON response that contains the reply text.
   * e.g. "summary", "data.reply", "choices.0.message.content"
   */
  @Input() responseKey = 'response';

  // ── UI ────────────────────────────────────────────────────────────────────
  /** Name shown in the chat header. */
  @Input() title = 'AI Assistant';
  /** First message shown when the chat opens. */
  @Input() welcome = 'Hi! How can I help you today?';
  /**
   * Suggestion chips shown before the first user message.
   * Pass a JSON array string: '["Question 1", "Question 2"]'
   */
  @Input() suggestions = '';
  /** Textarea placeholder text. */
  @Input() placeholder = 'Type your message...';

  @ViewChild('messagesEnd') messagesEnd!: ElementRef;
  private audioContext?: AudioContext;

  isOpen = signal(false);
  inputText = '';
  loading = signal(false);
  messages = signal<ChatMessage[]>([]);

  constructor(private el: ElementRef) {}

  ngOnInit(): void {
    this.messages.set([{ role: 'agent', text: this.welcome }]);
  }

  get parsedSuggestions(): string[] {
    if (!this.suggestions.trim()) return [];
    try { return JSON.parse(this.suggestions) as string[]; } catch { return []; }
  }

  get showSuggestions(): boolean {
    return this.messages().length === 1 && this.parsedSuggestions.length > 0 && !this.loading();
  }

  ngAfterViewChecked(): void {
    this.scrollToBottom();
  }

  toggle(): void {
    const next = !this.isOpen();
    this.isOpen.set(next);
    this.playToggleTone(next);
  }

  get canSend(): boolean {
    return this.inputText.trim().length >= 2 && !this.loading();
  }

  send(): void {
    if (!this.canSend) return;

    const userText = this.inputText.trim();
    this.inputText = '';

    this.messages.update(msgs => [...msgs, { role: 'user', text: userText }]);
    this.messages.update(msgs => [...msgs, { role: 'agent', text: '', loading: true }]);
    this.loading.set(true);
    this.primeAudio();

    this.callApi(userText)
      .then((raw) => {
        const text = this.extractText(raw) || JSON.stringify(raw);
        this.messages.update(msgs => [
          ...msgs.slice(0, -1),
          { role: 'agent', text },
        ]);
        this.loading.set(false);
        this.playCompletionTone();
        this.el.nativeElement.dispatchEvent(
          new CustomEvent('agentrix-response', { detail: raw, bubbles: true, composed: true })
        );
      })
      .catch((err: Error) => {
        this.messages.update(msgs => [
          ...msgs.slice(0, -1),
          { role: 'agent', text: `Error: ${err.message}` },
        ]);
        this.loading.set(false);
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

  // ── Helpers ───────────────────────────────────────────────────────────────

  private async callApi(query: string): Promise<Record<string, unknown>> {
    const url = `${this.apiUrl || ''}${this.endpoint}`;
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ [this.queryKey]: query }),
    });
    if (!res.ok) {
      const body = await res.json().catch(() => ({})) as { detail?: string; message?: string };
      throw new Error(body.detail ?? body.message ?? `HTTP ${res.status}`);
    }
    return res.json() as Promise<Record<string, unknown>>;
  }

  /**
   * Walk dot-notation path through the response object.
   * "data.reply" → response.data.reply
   * "choices.0.message.content" → response.choices[0].message.content
   */
  private extractText(obj: unknown): string {
    const parts = this.responseKey.split('.');
    let cur: unknown = obj;
    for (const part of parts) {
      if (cur == null || typeof cur !== 'object') return '';
      cur = (cur as Record<string, unknown>)[part];
    }
    return typeof cur === 'string' ? cur : '';
  }

  private scrollToBottom(): void {
    try {
      this.messagesEnd?.nativeElement?.scrollIntoView({ behavior: 'smooth' });
    } catch { /* ignore */ }
  }

  private primeAudio(): void {
    try { this.getAudioContext()?.resume(); } catch { /* ignore */ }
  }

  private playToggleTone(opened: boolean): void {
    const notes = opened
      ? [
          { frequency: 523.25, start: 0, duration: 0.07, volume: 0.06 },
          { frequency: 659.25, start: 0.07, duration: 0.1, volume: 0.07 },
        ]
      : [
          { frequency: 659.25, start: 0, duration: 0.06, volume: 0.055 },
          { frequency: 392, start: 0.06, duration: 0.11, volume: 0.06 },
        ];
    this.playTone(notes);
  }

  private playCompletionTone(): void {
    this.playTone([
      { frequency: 659.25, start: 0, duration: 0.08, volume: 0.08 },
      { frequency: 880, start: 0.09, duration: 0.12, volume: 0.08 },
    ]);
  }

  private playTone(notes: ToneNote[]): void {
    const context = this.getAudioContext();
    if (!context) return;

    const play = (): void => {
      for (const note of notes) {
        const oscillator = context.createOscillator();
        const gain = context.createGain();
        const startsAt = context.currentTime + note.start;
        const endsAt = startsAt + note.duration;

        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(note.frequency, startsAt);
        gain.gain.setValueAtTime(0.0001, startsAt);
        gain.gain.exponentialRampToValueAtTime(note.volume, startsAt + 0.015);
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
    const Ctor =
      window.AudioContext ||
      (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
    if (!Ctor) return undefined;
    this.audioContext = new Ctor();
    return this.audioContext;
  }
}
