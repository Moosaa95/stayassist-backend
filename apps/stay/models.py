from django.db import models
from django.conf import settings
from commons.mixins import ModelMixin


class Listing(ModelMixin):
    """Model for rental property listings"""

    title = models.CharField(max_length=200)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=100, db_index=True)
    max_guests = models.PositiveIntegerField(default=1)
    photos = models.JSONField(default=list, help_text="List of photo URLs")
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listings"
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["city", "created_at"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.city}"

    @classmethod
    def get_fields(cls):
        """Define fields to be returned when fetching listings"""
        return [
            "id",
            "title",
            "description",
            "price_per_night",
            "city",
            "photos",
            "host__first_name",
            "host__last_name",
            "host__email",
            "created_at",
            "updated_at",
            "max_guests",
        ]

    @classmethod
    def fetch_listings(cls, conditions=None):
        queryset = cls.objects.select_related("host")

        if conditions:
            queryset = queryset.filter(conditions)

        queryset = queryset.order_by("-pk").values(*cls.get_fields())

        return queryset

    @classmethod
    def get_listing(cls, **kwargs):
        """
        Get a single listing

        Args:
            obj: If True, return the object. If False, return values dict
            **kwargs: Filter parameters

        Returns:
            Listing object or dict
        """
        obj = kwargs.pop("obj", False)
        try:
            if obj:
                return cls.objects.select_related("host").get(**kwargs)
            else:
                return cls.objects.filter(**kwargs).values(*cls.get_fields()).first()
        except cls.DoesNotExist:
            return None


class Booking(ModelMixin):
    """Model for property bookings"""

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bookings"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()
    number_of_guests = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["listing", "check_in", "check_out"]),
        ]

    def __str__(self):
        return f"Booking for {self.listing.title} by {self.user.email}"

    def calculate_total_price(self):
        """Calculate total price based on number of nights"""
        nights = (self.check_out - self.check_in).days
        return self.listing.price_per_night * nights

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    @classmethod
    def get_fields(cls):
        """Define fields to be returned when fetching bookings"""
        return [
            "id",
            "listing__id",
            "listing__title",
            "listing__city",
            "user__id",
            "user__email",
            "check_in",
            "check_out",
            "number_of_guests",
            "total_price",
            "created_at",
        ]

    @classmethod
    def create_booking(cls, **kwargs):
        """
        Create a new booking

        Args:
            **kwargs: Booking parameters

        Returns:
            Booking object
        """
        try:
            # first check availability
            listing = Listing.get_listing(obj=True, id=kwargs.get("listing_id"))
            if not listing:
                return {"status": False, "message": "Listing not found"}
            overlapping_bookings = cls.objects.filter(
                listing=listing,
                check_in__lt=kwargs.get("check_out"),
                check_out__gt=kwargs.get("check_in"),
            )
            if overlapping_bookings.exists():
                return {
                    "status": False,
                    "message": "Listing is not available for the given dates",
                }
            booking = cls.objects.create(**kwargs)
            return {
                "status": True,
                # "booking": booking,
                "message": "Booking created successfully",
            }
        except Exception as e:
            return {"status": False, "message": str(e)}

    @classmethod
    def fetch_bookings(cls, values=False, conditions=None, count=100):
        """
        Fetch bookings with optional filters

        Args:
            values: If True, return values dict. If list, return specific fields
            conditions: Q object for filtering
            count: Limit number of results

        Returns:
            Queryset or list of dicts
        """
        if conditions:
            queryset = cls.objects.filter(conditions).select_related("listing", "user")
        else:
            queryset = cls.objects.all().select_related("listing", "user")

        queryset = queryset[:count]

        if values:
            if isinstance(values, list):
                return list(queryset.values(*values))
            else:
                return list(queryset.values(*cls.get_fields()))
        else:
            return queryset

    @classmethod
    def get_booking(cls, values=False, **kwargs):
        """
        Get a single booking

        Args:
            values: If True, return values dict
            **kwargs: Filter parameters

        Returns:
            Booking object or dict
        """
        try:
            if values:
                return cls.objects.filter(**kwargs).values(*cls.get_fields()).first()
            else:
                return cls.objects.select_related("listing", "user").get(**kwargs)
        except cls.DoesNotExist:
            return None
