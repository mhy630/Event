# admin.py
from django.contrib import admin
from .models import ContactFormEntry, Event, UserEventRegistration

@admin.register(ContactFormEntry)
class ContactFormEntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')
    search_fields = ('name', 'email', 'message')
    list_filter = ('name', 'email')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'location', 'event_type', 'status', 'user')
    search_fields = ('name', 'location', 'event_type', 'status', 'user__username')
    list_filter = ('event_type', 'status', 'user')

@admin.register(UserEventRegistration)
class UserEventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status')
    search_fields = ('user__username', 'event__name', 'status')
    list_filter = ('status', 'event__event_type', 'user__groups')
