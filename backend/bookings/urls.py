from django.urls import path
from .views import BookTicketView, MyBookingsView, EventBookingsView, CancelBookingView,export_bookings,user_recent_bookings

urlpatterns = [
    path('book-ticket/', BookTicketView.as_view()),                  # POST
    path('my-bookings/', MyBookingsView.as_view()),              # GET
    path('viewticketsofaevents/<int:pk>/', EventBookingsView.as_view()),  # GET for organizer
    path('cancel-bookings/<int:pk>/', CancelBookingView.as_view()),     # DELETE
    path('export-bookings/<str:format>/', export_bookings, name='export-bookings'),
    path('usersrecent-bookings/', user_recent_bookings, name='user-recent-bookings'),

]