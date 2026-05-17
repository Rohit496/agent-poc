import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { AgentApiService } from '../../services/agent-api.service';
import { QueryInputComponent } from '../../components/query-input/query-input.component';
import { AgentResponseComponent } from '../../components/agent-response/agent-response.component';
import { LoadingSpinnerComponent } from '../../components/loading-spinner/loading-spinner.component';
import { QueryRequest, QueryResponse } from '../../models/asset.model';

type QueryState = 'idle' | 'loading' | 'success' | 'error';

@Component({
  selector: 'app-query-page',
  standalone: true,
  imports: [CommonModule, QueryInputComponent, AgentResponseComponent, LoadingSpinnerComponent],
  templateUrl: './query-page.component.html',
  styleUrl: './query-page.component.scss',
})
export class QueryPageComponent {
  state = signal<QueryState>('idle');
  response = signal<QueryResponse | null>(null);
  errorMessage = signal<string | null>(null);

  constructor(private agentApi: AgentApiService) {}

  onQuerySubmit(req: QueryRequest): void {
    this.state.set('loading');
    this.errorMessage.set(null);

    this.agentApi.query(req).subscribe({
      next: (res) => {
        this.response.set(res);
        this.state.set('success');
      },
      error: (err: HttpErrorResponse) => {
        const msg = err.error?.detail ?? err.message ?? 'Unknown error';
        this.errorMessage.set(msg);
        this.state.set('error');
      },
    });
  }
}
