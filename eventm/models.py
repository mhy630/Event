# models.py
from django.contrib.auth.models import User
from django.db import models

class ContactFormEntry(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
    
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    event_type = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default='pending')  # Default status is 'pending'
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.id}: {self.name}: {self.status}"

class UserEventRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, default='pending')  # Status can be 'pending', 'approved', 'rejected', etc.

    def __str__(self):
        return f"{self.user.username} - {self.event.name} ({self.status})"
    
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    tickets_purchased = models.PositiveIntegerField(default=0)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"