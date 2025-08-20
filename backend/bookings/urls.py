
from django.urls import path
from .views import BookTicketView

urlpatterns = [
    path("book-ticket/", BookTicketView.as_view(), name="bookings"),
]

