import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Booking, BookingRequest } from '../models/booking.model';

@Injectable({ providedIn: 'root' })
export class BookingService {
  private readonly API_URL = 'http://localhost:8000/api/booking';

  constructor(private http: HttpClient) {}

  /**
   * Book tickets for an event
   * POST /api/booking/book-ticket/
   */
  bookTicket(data: BookingRequest): Observable<Booking> {
    return this.http.post<Booking>(`${this.API_URL}/book-ticket/`, data);
  }

  /**
   * Get bookings made by the current user
   * GET /api/booking/my-bookings/
   */
  getMyBookings(): Observable<Booking[]> {
    return this.http.get<Booking[]>(`${this.API_URL}/my-bookings/`);
  }

  /**
   * Cancel a booking by ID (user only)
   * DELETE /api/booking/cancel-bookings/<id>/
   */
  cancelBooking(id: number): Observable<any> {
    return this.http.delete(`${this.API_URL}/cancel-bookings/${id}/`);
  }

  /**
   * Organizer: View bookings for a specific event
   * GET /api/booking/viewticketsofaevents/<id>/
   */
  getEventBookings(eventId: number): Observable<Booking[]> {
    return this.http.get<Booking[]>(`${this.API_URL}/viewticketsofaevents/${eventId}/`);
  }

  /**
   * Export bookings for organizer events
   * GET /api/booking/export-bookings/<format>/
   * format: 'csv' or 'json'
   */
  exportBookings(format: 'csv' | 'json'): Observable<Blob | any> {
    return this.http.get(`${this.API_URL}/export-bookings/${format}/`, {
      responseType: format === 'csv' ? 'json' : 'json'
    });
  }

  /**
   * Get recent bookings of current user (last 10)
   * GET /api/booking/usersrecent-bookings/
   */
  getRecentUserBookings(): Observable<Booking[]> {
    return this.http.get<Booking[]>(`${this.API_URL}/usersrecent-bookings/`);
  }
}
