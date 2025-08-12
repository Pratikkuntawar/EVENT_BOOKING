import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { BookingService } from '../../../core/services/booking.service';
import { Booking } from '../../../core/models/booking.model';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { saveAs } from 'file-saver'

@Component({
  selector: 'app-event-bookings',
  standalone: true,
  imports: [CommonModule, MatTableModule, MatButtonModule, MatSnackBarModule],
  templateUrl: './event-bookings.html',
  styleUrls: ['./event-bookings.scss']
})
export class EventBookingsComponent implements OnInit {
  eventId!: number;
  bookings: Booking[] = [];
  displayedColumns = ['username', 'ticket_count', 'booked_at'];
  loading = false;

  constructor(
    private route: ActivatedRoute,
    private bookingService: BookingService,
    private snack: MatSnackBar
  ) {}

  ngOnInit(): void {
    const idParam = this.route.snapshot.paramMap.get('id');
    this.eventId = idParam ? +idParam : 0;
    if (this.eventId === 0) {
      this.snack.open('Invalid event ID', 'Close', { duration: 3000 });
      return;
    }
    this.loadBookings();
  }

  loadBookings(): void {
    this.loading = true;
    this.bookingService.getEventBookings(this.eventId).subscribe({
      next: (data) => {
        this.bookings = data;
        this.loading = false;
      },
      error: () => {
        this.snack.open('Error loading bookings', 'Close', { duration: 3000 });
        this.loading = false;
      }
    });
  }

  exportBookings(format: 'csv' | 'json'): void {
    this.bookingService.exportBookings(format).subscribe({
      next: (res) => {
        if (format === 'csv' && res instanceof Blob) {
          saveAs(res, `bookings_event_${this.eventId}.csv`);
        } else {
          this.snack.open('Exported data received', 'Close', { duration: 3000 });
        }
      },
      error: () => {
        this.snack.open('Failed to export bookings', 'Close', { duration: 3000 });
      }
    });
  }
}
