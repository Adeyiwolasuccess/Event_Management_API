# events/models.py
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class EventCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(EventCategory, on_delete=models.PROTECT, related_name='events')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    capacity = models.PositiveIntegerField(default=0)  # 0 = unlimited
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def clean(self):
        # Prevent creating/updating events in the past
        if self.date and self.date < timezone.now():
            raise ValidationError({'date': 'Event date must be in the future.'})

    def seats_taken(self):
        return self.registrations.filter(status=Registration.Status.REGISTERED).count()

    def seats_available(self):
        if self.capacity == 0:
            return None  # unlimited
        return max(self.capacity - self.seats_taken(), 0)

    def is_full(self):
        if self.capacity == 0:
            return False
        return self.seats_taken() >= self.capacity

    def __str__(self):
        return f"{self.title} @ {self.date}"


class TicketPricing(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.CharField(max_length=80)  # VIP, Regular etc
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')

    class Meta:
        unique_together = ('event', 'ticket_type')

    def __str__(self):
        return f"{self.ticket_type} - {self.price} {self.currency}"


class Registration(models.Model):
    class Status(models.TextChoices):
        REGISTERED = 'registered', 'Registered'
        ATTENDED = 'attended', 'Attended'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REGISTERED)
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')  # a user can register once per event

    def clean(self):
        # Can't register to past events
        if self.event.date and self.event.date < timezone.now():
            raise ValidationError("Cannot register for an event that already happened.")

        # Prevent registration when event is full
        if self._state.adding and self.event.is_full():
            raise ValidationError("Event is fully booked.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} -> {self.event} ({self.status})"

class TicketPricing(models.Model):
        event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets")
        ticket_type = models.CharField(max_length=50)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        currency = models.CharField(max_length=10, default="USD")

def __str__(self):
        return f"{self.ticket_type} - {self.price} {self.currency} ({self.event.title})"
