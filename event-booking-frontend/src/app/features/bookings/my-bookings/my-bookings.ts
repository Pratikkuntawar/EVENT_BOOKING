import { Component, OnInit } from '@angular/core';
import { BookingService } from '../../../core/services/booking.service';
import { Booking } from '../../../core/models/booking.model';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';

@Component({
  selector: 'app-my-bookings',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatButtonModule, MatSnackBarModule],
  templateUrl: './my-bookings.html',
  styleUrl: './my-bookings.scss'
})
export class MyBookingsComponent implements OnInit {
  bookings: Booking[] = [];

  constructor(private bookingService: BookingService, private snack: MatSnackBar) {}

  ngOnInit() {
    this.loadBookings();
  }

  loadBookings() {
    this.bookingService.getMyBookings().subscribe(data => this.bookings = data);
  }

  cancelBooking(id: number) {
    this.bookingService.cancelBooking(id).subscribe({
      next: () => {
        this.snack.open('Booking cancelled', 'Close', { duration: 3000 });
        this.loadBookings();
      },
      error: () => {
        this.snack.open('Error cancelling booking', 'Close', { duration: 3000 });
      }
    });
  }
}
