from django.db import models
from users.models import CustomUser  # adjust based on your user model location

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    category = models.CharField(max_length=100)
    ticket_price=models.DecimalField()
    total_tickets = models.PositiveIntegerField()
    tickets_remaining = models.PositiveIntegerField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='organized_events')
    image_url = models.URLField(max_length=500,default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2hsa5aYA0NfcvhScC8i3nm4EO0G93eaolqA&s")  # Replace with your default hosted image
    

    def save(self, *args, **kwargs):
        if not self.pk:  # on create
            self.tickets_remaining = self.total_tickets
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
