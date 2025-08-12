import { Routes } from '@angular/router';
import { LoginComponent } from './features/auth/login/login';
import { RegisterComponent } from './features/auth/register/register';
import { EventListComponent } from './features/events/event-list/event-list';
import { EventDetailComponent } from './features/events/event-detail/event-detail';
import { MyBookingsComponent } from './features/bookings/my-bookings/my-bookings';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'events', component: EventListComponent },
  { path: '', pathMatch: 'full', redirectTo: 'events' },
  { path: 'events/:id', component: EventDetailComponent },
  { path: 'my-bookings', component: MyBookingsComponent },
];
