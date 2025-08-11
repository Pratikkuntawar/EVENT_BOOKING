from django.db import models
from django.conf import settings
from events.models import Event

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_count = models.PositiveIntegerField()
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} booked {self.ticket_count} for {self.event.title}"
