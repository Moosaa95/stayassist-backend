from rest_framework import serializers
from datetime import date
from stay.models import Listing, Booking


# ==================== Listing Serializers ====================
class BookingSerializer(serializers.Serializer):
    """Serializer for booking information within listing details"""

    id = serializers.UUIDField(
        read_only=True, help_text="Unique identifier for the booking."
    )
    user_id = serializers.UUIDField(
        read_only=True, help_text="The user who made the booking."
    )
    check_in = serializers.DateField(help_text="Check-in date.")
    check_out = serializers.DateField(help_text="Check-out date.")
    number_of_guests = serializers.IntegerField(help_text="Number of guests.")
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, help_text="Total price for the booking."
    )
    created_at = serializers.DateTimeField(
        read_only=True, help_text="Date and time the booking was created."
    )


class ListingFilterSerializer(serializers.Serializer):
    """Filter serializer for listing queries"""

    city = serializers.CharField(
        required=False, help_text="Filter by city name (case-insensitive)."
    )
    check_in = serializers.DateField(
        required=False, help_text="Check-in date for availability (YYYY-MM-DD)."
    )
    check_out = serializers.DateField(
        required=False, help_text="Check-out date for availability (YYYY-MM-DD)."
    )


class FetchListingsSerializer(serializers.Serializer):
    """Request serializer for fetching listings with filters"""

    filters = ListingFilterSerializer(
        required=False, help_text="Optional filters for listing queries."
    )
    count = serializers.IntegerField(
        required=False, help_text="Limit the number of listings returned."
    )


class ListingSerializer(serializers.Serializer):
    """Response serializer for listing data"""

    id = serializers.UUIDField(
        read_only=True, help_text="Unique identifier for the listing."
    )
    title = serializers.CharField(
        max_length=200, help_text="Title of the rental property."
    )
    description = serializers.CharField(
        help_text="Detailed description of the property."
    )
    price_per_night = serializers.DecimalField(
        max_digits=10, decimal_places=2, help_text="Price per night in USD."
    )
    city = serializers.CharField(
        max_length=100, help_text="City where the property is located."
    )
    photos = serializers.ListField(
        child=serializers.URLField(),
        required=False,
        help_text="List of photo URLs for the property.",
    )
    host_name = serializers.CharField(
        read_only=True, help_text="Full name of the property host."
    )
    host_email = serializers.CharField(
        read_only=True, help_text="Email address of the property host."
    )
    created_at = serializers.DateTimeField(
        read_only=True, help_text="Date and time the listing was created."
    )
    updated_at = serializers.DateTimeField(
        read_only=True, help_text="Date and time the listing was last updated."
    )


class ListingDetailRequestSerializer(serializers.Serializer):
    """Request serializer for fetching detailed listing information"""

    id = serializers.UUIDField(
        required=True, help_text="The unique identifier of the listing."
    )


class ListingDetailSerializer(serializers.Serializer):
    """Response serializer for detailed listing information"""

    id = serializers.UUIDField(
        read_only=True, help_text="Unique identifier for the listing."
    )
    title = serializers.CharField(
        max_length=200, help_text="Title of the rental property."
    )
    description = serializers.CharField(
        help_text="Detailed description of the property."
    )
    price_per_night = serializers.DecimalField(
        max_digits=10, decimal_places=2, help_text="Price per night in USD."
    )
    city = serializers.CharField(
        max_length=100, help_text="City where the property is located."
    )
    photos = serializers.ListField(
        child=serializers.URLField(), help_text="List of photo URLs for the property."
    )
    host_name = serializers.CharField(
        read_only=True, help_text="Full name of the property host."
    )
    host_email = serializers.CharField(
        read_only=True, help_text="Email address of the property host."
    )
    total_bookings = serializers.IntegerField(
        read_only=True, help_text="Total number of bookings for this listing."
    )
    created_at = serializers.DateTimeField(
        read_only=True, help_text="Date and time the listing was created."
    )
    updated_at = serializers.DateTimeField(
        read_only=True, help_text="Date and time the listing was last updated."
    )


# ==================== Booking Serializers ====================


class BookingFilterSerializer(serializers.Serializer):
    """Filter serializer for booking queries"""

    listing_id = serializers.UUIDField(
        required=False, help_text="Filter by listing ID."
    )
    user_id = serializers.UUIDField(required=False, help_text="Filter by user ID.")
    check_in = serializers.DateField(
        required=False, help_text="Filter by check-in date (YYYY-MM-DD)."
    )
    check_out = serializers.DateField(
        required=False, help_text="Filter by check-out date (YYYY-MM-DD)."
    )
    start_date = serializers.DateField(
        required=False, help_text="Filter bookings from this date onwards (YYYY-MM-DD)."
    )
    end_date = serializers.DateField(
        required=False, help_text="Filter bookings up to this date (YYYY-MM-DD)."
    )
    count = serializers.IntegerField(
        required=False, help_text="Limit the number of results returned."
    )


class FetchBookingsSerializer(serializers.Serializer):
    """Request serializer for fetching bookings with filters"""

    filters = BookingFilterSerializer(
        required=False, help_text="Optional filters for booking queries."
    )


class CreateBookingSerializer(serializers.Serializer):
    """Request serializer for creating a new booking"""

    listing_id = serializers.UUIDField(
        required=True, help_text="The unique identifier of the listing to book."
    )
    check_in = serializers.DateField(
        required=True, help_text="Check-in date (YYYY-MM-DD)."
    )
    check_out = serializers.DateField(
        required=True, help_text="Check-out date (YYYY-MM-DD)."
    )
    number_of_guests = serializers.IntegerField(
        min_value=1, required=True, help_text="Number of guests for the booking."
    )
    user = serializers.UUIDField(
        required=True, help_text="The user making the booking."
    )

    def validate_check_in(self, value):
        """Validate check-in date is not in the past"""
        if value < date.today():
            raise serializers.ValidationError("Check-in date cannot be in the past")
        return value

    def validate(self, data):
        """Validate check-out is after check-in"""
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError(
                "Check-out date must be after check-in date"
            )
        return data


class BookingSerializer(serializers.Serializer):
    """Response serializer for booking data"""

    id = serializers.UUIDField(
        read_only=True, help_text="Unique identifier for the booking."
    )
    listing_id = serializers.UUIDField(
        read_only=True, help_text="The listing that was booked."
    )
    listing_title = serializers.CharField(
        read_only=True, help_text="Title of the booked listing."
    )
    listing_city = serializers.CharField(
        read_only=True, help_text="City of the booked listing."
    )
    user_id = serializers.UUIDField(
        read_only=True, help_text="The user who made the booking."
    )
    user_email = serializers.CharField(
        read_only=True, help_text="Email of the user who made the booking."
    )
    check_in = serializers.DateField(help_text="Check-in date.")
    check_out = serializers.DateField(help_text="Check-out date.")
    number_of_guests = serializers.IntegerField(help_text="Number of guests.")
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, help_text="Total price for the booking."
    )
    created_at = serializers.DateTimeField(
        read_only=True, help_text="Date and time the booking was created."
    )


# ==================== Search Serializers ====================


class SearchListingsSerializer(serializers.Serializer):
    """Request serializer for searching listings"""

    city = serializers.CharField(
        required=True, help_text="City to search for listings (required)."
    )
    check_in = serializers.DateField(
        required=False, help_text="Check-in date for availability check (YYYY-MM-DD)."
    )
    check_out = serializers.DateField(
        required=False, help_text="Check-out date for availability check (YYYY-MM-DD)."
    )
    min_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        help_text="Minimum price per night.",
    )
    max_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        help_text="Maximum price per night.",
    )

    def validate(self, data):
        """Validate date ranges if provided"""
        check_in = data.get("check_in")
        check_out = data.get("check_out")

        if check_in and check_out:
            if check_out <= check_in:
                raise serializers.ValidationError(
                    "Check-out date must be after check-in date"
                )

        return data
