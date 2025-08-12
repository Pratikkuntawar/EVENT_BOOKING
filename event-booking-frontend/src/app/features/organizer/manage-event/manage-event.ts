import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ActivatedRoute, Router } from '@angular/router';
import { EventService } from '../../../core/services/event.service';
import { EVENT_CATEGORIES, Event } from '../../../core/models/event.model';
import { CreateEventRequest } from '../../../core/models/event.model';

@Component({
  selector: 'app-manage-event',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    MatSnackBarModule
  ],
  templateUrl: './manage-event.html',
  styleUrls: ['./manage-event.scss']
})
export class ManageEventComponent implements OnInit {
  

  categories = EVENT_CATEGORIES;
  editMode = false;
  eventId?: number;
  form;

  constructor(
    private fb: FormBuilder,
    private eventService: EventService,
    private snack: MatSnackBar,
    private route: ActivatedRoute,
    private router: Router
  ) {
    this.form = this.fb.group({
    title: ['', Validators.required],
    description: ['', Validators.required],
    location: ['', Validators.required],
    datetime: ['', Validators.required],
    category: ['', Validators.required],
    ticket_price: [0, Validators.required],
    total_tickets: [0, Validators.required],
    image_url: ['']
  });
  }

  ngOnInit(): void {
    this.eventId = Number(this.route.snapshot.paramMap.get('id'));
    if (this.eventId) {
      this.editMode = true;
      this.eventService.getEventById(this.eventId).subscribe(event => {
        this.form.patchValue(event);
      });
    }
  }

 submit(): void {
  if (this.form.invalid) return;

  const payload: CreateEventRequest = {
    title: this.form.value.title!,
    description: this.form.value.description!,
    location: this.form.value.location!,
    datetime: this.form.value.datetime!,
    category: this.form.value.category!,
    ticket_price: this.form.value.ticket_price!,
    total_tickets: this.form.value.total_tickets!,
    image_url: this.form.value.image_url || undefined
  };

  const apiCall = this.editMode && this.eventId
    ? this.eventService.updateEvent(this.eventId, payload)
    : this.eventService.createEvent(payload);

  apiCall.subscribe({
    next: () => {
      this.snack.open(`Event ${this.editMode ? 'updated' : 'created'} successfully`, 'Close', { duration: 3000 });
      this.router.navigate(['/organizer/dashboard']);
    },
    error: () => this.snack.open('Error saving event', 'Close', { duration: 3000 })
  });
}

}
