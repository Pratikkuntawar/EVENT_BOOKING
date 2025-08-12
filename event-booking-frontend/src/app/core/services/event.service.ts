import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Event, CreateEventRequest } from '../models/event.model';

@Injectable({ providedIn: 'root' })
export class EventService {
  private readonly API_URL = 'http://localhost:8000/api/events';

  constructor(private http: HttpClient) {}

  /**
   * Public events listing with optional category/search
   */
  getAllEvents(category?: string, search?: string): Observable<Event[]> {
    let params = new HttpParams();
    if (category) params = params.set('category', category);
    if (search) params = params.set('search', search);

    return this.http.get<Event[]>(`${this.API_URL}/listallevents/`, { params });
  }

  /**
   * Single event details
   */
  getEventById(id: number): Observable<Event> {
    return this.http.get<Event>(`${this.API_URL}/detailsofaevent/${id}/`);
  }

  /**
   * Organizer's own events
   */
  getMyEvents(): Observable<Event[]> {
    return this.http.get<Event[]>(`${this.API_URL}/my-events/`);
  }

  /**
   * Create a new event (only organizers)
   */
  createEvent(event: CreateEventRequest): Observable<Event> {
    return this.http.post<Event>(`${this.API_URL}/create-event/`, event);
  }

  /**
   * Update event by ID (only organizers)
   */
  updateEvent(id: number, event: Partial<CreateEventRequest>): Observable<Event> {
    return this.http.put<Event>(`${this.API_URL}/update-events/${id}/`, event);
  }

  /**
   * Delete event by ID (only organizers)
   */
  deleteEvent(id: number): Observable<any> {
    return this.http.delete(`${this.API_URL}/delete-events/${id}/`);
  }
}
