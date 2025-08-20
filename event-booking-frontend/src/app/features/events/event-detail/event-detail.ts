import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatSelectModule } from '@angular/material/select';
import { FormsModule } from '@angular/forms';
import { EventService } from '../../../core/services/event.service';
import { BookingService } from '../../../core/services/booking.service';
import { Event } from '../../../core/models/event.model';

@Component({
  selector: 'app-event-detail',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatCardModule,
    MatButtonModule,
    MatSnackBarModule,
    MatSelectModule,
    FormsModule
  ],
  templateUrl: './event-detail.html',
  styleUrls: ['./event-detail.scss']
})
export class EventDetailComponent implements OnInit {
  event?: Event;
  loading = false;
  ticketQuantity = 1;
  ticketsArray;

  constructor(
    private route: ActivatedRoute,
    private eventService: EventService,
    private bookingService: BookingService,
    private snack: MatSnackBar,
    private router: Router
  ) {

  this.ticketsArray = Array.from(
  { length: Number(this.event?.tickets_remaining) },
  (_, i) => i + 1
);
  }


  ngOnInit(): void {
    const idParam = this.route.snapshot.paramMap.get('id');
    const id = idParam ? +idParam : null;
    if (id === null) {
      this.snack.open('Invalid event ID', 'Close', { duration: 3000 });
      this.router.navigate(['/events']);
      return;
    }
    this.loadEvent(id);
  }

  loadEvent(id: number): void {
    this.loading = true;
    this.eventService.getEventById(id).subscribe({
      next: (data) => {
        this.event = data;
        this.loading = false;
        // Reset ticket quantity on new event load
        this.ticketQuantity = 1;
      },
      error: () => {
        this.snack.open('Error loading event', 'Close', { duration: 3000 });
        this.loading = false;
        this.router.navigate(['/events']);
      }
    });
  }

  confirmBooking(): void {
    if (!this.event) return;

    if (this.ticketQuantity < 1 || this.ticketQuantity > this.event.tickets_remaining) {
      this.snack.open(`Please select a ticket quantity between 1 and ${this.event.tickets_remaining}`, 'Close', { duration: 4000 });
      return;
    }

    const confirmed = window.confirm(`Confirm booking of ${this.ticketQuantity} ticket(s) for event "${this.event.title}"?`);
    if (!confirmed) return;

    this.bookingService.bookTicket({
      event_id: this.event.id,
      ticket_count: this.ticketQuantity
    }).subscribe({
      next: () => {
        this.snack.open('Booking successful!', 'Close', { duration: 3000 });
        this.router.navigate(['/my-bookings']);
      },
      error: (error) => {
        const msg = error.error?.error || 'Booking failed. Please try again.';
        this.snack.open(msg, 'Close', { duration: 4000 });
      }
    });
  }
}
