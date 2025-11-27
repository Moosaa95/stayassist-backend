from django.contrib import admin
from stay.models import Listing, Booking


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'city', 'price_per_night', 'host', 'created_at']
    list_filter = ['city', 'created_at']
    search_fields = ['title', 'city', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['listing', 'user', 'check_in', 'check_out', 'number_of_guests', 'total_price', 'created_at']
    list_filter = ['check_in', 'check_out', 'created_at']
    search_fields = ['listing__title', 'user__email']
    readonly_fields = ['id', 'total_price', 'created_at', 'updated_at']
