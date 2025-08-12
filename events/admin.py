# events/admin.py
from django.contrib import admin
from .models import EventCategory, Event, TicketPricing, Registration

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date', 'location', 'category', 'created_by', 'capacity')
    list_filter = ('category', 'date')
    search_fields = ('title', 'location', 'description')

@admin.register(TicketPricing)
class TicketPricingAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'ticket_type', 'price', 'currency')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'event', 'status', 'registration_date')
    list_filter = ('status',)

