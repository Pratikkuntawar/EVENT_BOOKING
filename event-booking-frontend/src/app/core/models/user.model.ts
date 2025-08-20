export interface User {
  username: string;
  email: string;
  role: 'Organizer' | 'User';
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  role: 'Organizer' | 'User';
}

export interface AuthResponse {
  access: string;
  refresh: string;
  role: string;
  username: string;
}
