
from django.urls import path
from .views import EventUnifiedView

urlpatterns = [
    path('events/', EventUnifiedView.as_view()),            # For list, create
    path('events/<int:pk>/', EventUnifiedView.as_view()),    # For detail, update, delete
]

