export interface Event {
  id: number;
  title: string;
  description: string;
  location: string;
  datetime: string; // ISO Date string
  category: string;
  ticket_price: number;
  total_tickets: number;
  tickets_remaining: number;
  image_url: string;
  organizer: {
    id: number;
    username: string;
    email: string;
  };
}

/**
 * Matches the fields your Django CreateEventView expects.
 * 'organizer' and 'tickets_remaining' are excluded because the backend sets them.
 */
export interface CreateEventRequest {
  title: string;
  description: string;
  location: string;
  datetime: string; // ISO date string format
  category: string;
  ticket_price: number;
  total_tickets: number;
  image_url?: string; // optional if backend sets a default
}

export const EVENT_CATEGORIES = [
  'Concerts',
  'Sports',
  'Comedy',
  'Theatre',
  'Workshops',
  'Conferences',
  'Food & Drink',
  'Art & Culture',
  'Technology',
  'Business'
] as const;
