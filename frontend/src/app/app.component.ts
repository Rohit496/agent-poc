import { Component, CUSTOM_ELEMENTS_SCHEMA, OnInit, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { AssetStateService } from './services/asset-state.service';
import { QueryResponse } from './models/asset.model';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  template: `
    <router-outlet />
    <agentrix-chat
      title="Agentrix Assistant"
      welcome="Hi! I'm your asset intelligence assistant. Ask me anything — include a Party Number like P-10042 and I'll find the assets for you."
      suggestions='["Show me all active servers for P-10042","List all hardware in DC-East for P-20017","Which servers are in maintenance for P-30099?","Show all assets for P-20017"]'
      placeholder="e.g. Show servers for P-10042..."
      endpoint="/api/query"
      query-key="query"
      response-key="summary"
    ></agentrix-chat>
  `,
})
export class AppComponent implements OnInit {
  private assetState = inject(AssetStateService);

  ngOnInit(): void {
    window.addEventListener('agentrix-response', (event: Event) => {
      const detail = (event as CustomEvent<QueryResponse>).detail;
      this.assetState.setResponse(detail.party_number, detail);
    });
  }
}
