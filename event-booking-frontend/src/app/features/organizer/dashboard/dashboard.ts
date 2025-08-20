import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { RouterModule, Router } from '@angular/router';
import { EventService } from '../../../core/services/event.service';
import { Event } from '../../../core/models/event.model';

@Component({
  selector: 'app-organizer-dashboard',
  standalone: true,
  imports: [CommonModule, MatTableModule, MatButtonModule, RouterModule, MatSnackBarModule],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.scss']
})
export class DashboardComponent implements OnInit {
  displayedColumns = ['title', 'datetime', 'tickets_remaining', 'price', 'actions'];
  myEvents: Event[] = [];

  constructor(
    private eventService: EventService,
    private snack: MatSnackBar,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadMyEvents();
  }

  loadMyEvents(): void {
    this.eventService.getMyEvents().subscribe({
      next: (data) => this.myEvents = data,
      error: () => this.snack.open('Error loading events', 'Close', { duration: 3000 })
    });
  }

  editEvent(id: number): void {
    this.router.navigate(['/organizer/edit-event', id]);
  }

  deleteEvent(id: number): void {
    if (!confirm('Delete this event?')) return;
    this.eventService.deleteEvent(id).subscribe({
      next: () => {
        this.snack.open('Event deleted', 'Close', { duration: 3000 });
        this.loadMyEvents();
      },
      error: () => this.snack.open('Error deleting event', 'Close', { duration: 3000 })
    });
  }
}
