from django.urls import path
from stay.views import (
    ListingListAPIView,
    ListingDetailAPIView,
    # SearchListingsAPIView,
    BookingCreateAPIView,
    # UserBookingsAPIView
)

app_name = "stay"

urlpatterns = [
    # Listing endpoints
    path("listings/", ListingListAPIView.as_view(), name="listing-list"),
    # path('listings/search/', SearchListingsAPIView.as_view(), name='listing-search'),
    path("get_listing/", ListingDetailAPIView.as_view(), name="listing-detail"),
    # Booking endpoints
    path("bookings/", BookingCreateAPIView.as_view(), name="booking-create"),
    # path('bookings/my-bookings/', UserBookingsAPIView.as_view(), name='user-bookings'),
]
