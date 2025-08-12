import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Event } from '../models/event.model';

@Injectable({ providedIn: 'root' })
export class EventService {
  private readonly API_URL = 'http://localhost:8000/api/events';

  constructor(private http: HttpClient) {}

  getAllEvents(category?: string, search?: string): Observable<Event[]> {
    let params = new HttpParams();
    if (category) params = params.set('category', category);
    if (search) params = params.set('search', search);

    return this.http.get<Event[]>(`${this.API_URL}/listallevents/`, { params });
  }
}
