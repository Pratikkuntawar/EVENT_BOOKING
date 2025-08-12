import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Booking, BookingRequest } from '../models/booking.model';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class BookingService {
  private readonly API_URL = 'http://localhost:8000/api/booking';

  constructor(private http: HttpClient) {}

  bookTicket(data: BookingRequest): Observable<Booking> {
    return this.http.post<Booking>(`${this.API_URL}/book-ticket/`, data);
  }

  getMyBookings(): Observable<Booking[]> {
    return this.http.get<Booking[]>(`${this.API_URL}/my-bookings/`);
  }

  cancelBooking(id: number): Observable<any> {
    return this.http.delete(`${this.API_URL}/cancel-bookings/${id}/`);
  }
}
