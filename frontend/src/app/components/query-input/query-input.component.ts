import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { QueryRequest } from '../../models/asset.model';

@Component({
  selector: 'app-query-input',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './query-input.component.html',
  styleUrl: './query-input.component.scss',
})
export class QueryInputComponent {
  @Output() querySubmit = new EventEmitter<QueryRequest>();

  partyNumber = '';
  query = '';

  get isValid(): boolean {
    return /^P-\d+$/.test(this.partyNumber) && this.query.trim().length >= 3;
  }

  onSubmit(): void {
    if (this.isValid) {
      this.querySubmit.emit({ party_number: this.partyNumber, query: this.query.trim() });
    }
  }
}
