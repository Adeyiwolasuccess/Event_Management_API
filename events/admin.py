from django.contrib import admin
from .models import EventCategory, Event, TicketPricing

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date', 'location', 'created_by')

@admin.register(TicketPricing)
class TicketPricingAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'ticket_type', 'price', 'currency')
