import { Routes } from '@angular/router';
import { LoginComponent } from './features/auth/login/login';
import { RegisterComponent } from './features/auth/register/register';
import { EventListComponent } from './features/events/event-list/event-list';
import { EventDetailComponent } from './features/events/event-detail/event-detail';
import { MyBookingsComponent } from './features/bookings/my-bookings/my-bookings';
import { DashboardComponent } from './features/organizer/dashboard/dashboard';
import { ManageEventComponent } from './features/organizer/manage-event/manage-event';
import { EventBookingsComponent } from './features/organizer/event-bookings/event-bookings';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'events', component: EventListComponent },
  { path: '', pathMatch: 'full', redirectTo: 'events' },
  { path: 'events/:id', component: EventDetailComponent },
  { path: 'my-bookings', component: MyBookingsComponent },
   { path: 'organizer/dashboard', component: DashboardComponent },
  { path: 'organizer/create-event', component: ManageEventComponent },
  { path: 'organizer/edit-event/:id', component: ManageEventComponent },
   { path: 'organizer/event-bookings/:id', component: EventBookingsComponent },
];

