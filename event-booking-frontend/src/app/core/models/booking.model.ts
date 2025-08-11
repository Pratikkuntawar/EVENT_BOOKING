import { Event } from './event.model';

export interface Booking {
  id: number;
  event: Event;
  ticket_count: number;
  booked_at: string;
}

export interface BookingRequest {
  event_id: number;
  ticket_count: number;
}
