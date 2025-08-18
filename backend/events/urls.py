# from django.urls import path
# from .views import (
#     EventListView, EventDetailView, MyEventsView,
#     CreateEventView, UpdateEventView, DeleteEventView
# )

# urlpatterns = [
#     path('listallevents/', EventListView.as_view()),
#     path('detailsofaevent/<int:pk>/', EventDetailView.as_view()),
#     path('my-events/', MyEventsView.as_view()),
#     path('create-event/', CreateEventView.as_view()),
#     path('update-events/<int:pk>/', UpdateEventView.as_view()),
#     path('delete-events/<int:pk>/', DeleteEventView.as_view()),
# ]

from django.urls import path
from .views import EventUnifiedView

urlpatterns = [
    path('events/', EventUnifiedView.as_view()),            # For list, create
    path('events/<int:pk>/', EventUnifiedView.as_view()),    # For detail, update, delete
]

