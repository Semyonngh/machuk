from django.contrib import admin
from .models import Category, Artist, Venue, Concert, Ticket, TicketOrder

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'genre']
    search_fields = ['name']
    list_filter = ['genre']

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'capacity']
    list_filter = ['city']
    search_fields = ['name', 'city']

@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    list_display = ['artist', 'venue', 'start_time', 'end_time']
    list_filter = ['venue__city', 'start_time']
    search_fields = ['artist__name', 'venue__city']
    date_hierarchy = 'start_time'

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['concert', 'category_id', 'price', 'quantity', 'date']
    list_filter = ['category_id', 'date']
    search_fields = ['concert__artist__name']

@admin.register(TicketOrder)
class TicketOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_name', 'concert', 'ticket_type', 'quantity', 'total_price', 'order_date']
    list_filter = ['ticket_type', 'order_date']
    search_fields = ['customer_name', 'order_number']
    readonly_fields = ['order_number', 'order_date']