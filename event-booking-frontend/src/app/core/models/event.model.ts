export interface Event {
  id: number;
  title: string;
  description: string;
  location: string;
  datetime: string;
  category: string;
  ticket_price: number;
  total_tickets: number;
  tickets_remaining: number;
  image_url: string;
  organizer: {
    username: string;
    email: string;
  };
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
];
