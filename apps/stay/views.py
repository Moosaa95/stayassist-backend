from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from drf_spectacular.utils import extend_schema, inline_serializer

from stay.models import Listing, Booking
from stay.serializers import (
    ListingDetailRequestSerializer,
    ListingSerializer,
    ListingDetailSerializer,
    BookingSerializer,
    FetchListingsSerializer,
    SearchListingsSerializer,
    CreateBookingSerializer,
    FetchBookingsSerializer,
)


class ListingListAPIView(APIView):
    """Fetch all rental listings with optional filters"""

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Listings"],
        description="Fetch all rental listings with optional filters for city, dates, and price range",
        request=FetchListingsSerializer,
        responses={
            200: inline_serializer(
                name="FetchListingsResponse",
                fields=dict(
                    status=serializers.BooleanField(),
                    message=serializers.CharField(),
                    data=ListingSerializer(many=True),
                    count=serializers.IntegerField(),
                ),
            ),
        },
    )
    def post(self, request):
        serializer = FetchListingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated = serializer.validated_data.get("filters", {})
        condition = Q()

        if "city" in validated:
            condition &= Q(city__iexact=validated["city"])

        # Availability filter using date exclusion
        if "check_in" in validated and "check_out" in validated:
            check_in = validated["check_in"]
            check_out = validated["check_out"]

            # remove listings with overlapping bookings
            condition &= ~Q(
                bookings__check_in__lt=check_out,
                bookings__check_out__gt=check_in,
                bookings__status__in=["pending", "confirmed"],
            )

        listings = Listing.fetch_listings(conditions=condition)

        return Response(
            {
                "status": True,
                "message": "Listings fetched successfully",
                "data": listings,
            },
            status=status.HTTP_200_OK,
        )


class ListingDetailAPIView(APIView):
    """Get detailed information about a specific listing"""

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Listings"],
        description="Get detailed information about a specific listing including booking count",
        request=inline_serializer(
            name="ListingDetailRequest",
            fields=dict(
                id=serializers.UUIDField(
                    required=True, help_text="The unique identifier of the listing."
                )
            ),
        ),
        responses={
            200: inline_serializer(
                name="ListingDetailResponse",
                fields=dict(
                    status=serializers.BooleanField(),
                    message=serializers.CharField(),
                    data=ListingDetailSerializer(),
                ),
            ),
        },
    )
    def post(self, request):
        """Get listing details"""
        serializers = ListingDetailRequestSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)

        listing_id = serializers.validated_data.get("id")

        listing_data = Listing.get_listing(id=listing_id)

        if not listing_data:
            return Response(
                data=dict(status=False, message="Listing not found", data=None),
                status=status.HTTP_404_NOT_FOUND,
            )

        # Get booking count
        total_bookings = Booking.objects.filter(listing_id=listing_id).count()
        listing_data["total_bookings"] = total_bookings

        return Response(
            data=dict(
                status=True,
                message="Listing details retrieved successfully",
                data=listing_data,
            ),
            status=status.HTTP_200_OK,
        )


# class SearchListingsAPIView(APIView):
#     """Search listings by city with optional availability and price filters"""

#     permission_classes = [AllowAny]

#     @extend_schema(
#         tags=["Listings"],
#         description="Search rental listings by city with optional filters for availability dates and price range",
#         request=SearchListingsSerializer,
#         responses={
#             200: inline_serializer(
#                 name="SearchListingsResponse",
#                 fields=dict(
#                     status=serializers.BooleanField(),
#                     message=serializers.CharField(),
#                     data=ListingSerializer(many=True),
#                     count=serializers.IntegerField(),
#                 ),
#             ),
#         },
#     )
#     def post(self, request):
#         """Search listings by city and availability"""
#         serializer = SearchListingsSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         city = serializer.validated_data.get("city")
#         check_in = serializer.validated_data.get("check_in")
#         check_out = serializer.validated_data.get("check_out")
#         min_price = serializer.validated_data.get("min_price")
#         max_price = serializer.validated_data.get("max_price")

#         # Build Q object for conditions
#         conditions = Q(city__icontains=city)

#         # Apply price filters
#         if min_price:
#             conditions.add(Q(price_per_night__gte=min_price), Q.AND)

#         if max_price:
#             conditions.add(Q(price_per_night__lte=max_price), Q.AND)

#         # If dates provided, exclude listings with overlapping bookings
#         if check_in and check_out:
#             # Get listings with overlapping bookings
#             booked_listing_ids = Booking.objects.filter(
#                 check_in__lt=check_out, check_out__gt=check_in
#             ).values_list("listing_id", flat=True)

#             # Exclude booked listings
#             if booked_listing_ids:
#                 conditions.add(~Q(id__in=booked_listing_ids), Q.AND)

#         # Fetch listings using class method
#         listings_data = Listing.fetch_listings(
#             values=True, conditions=conditions, count=100
#         )

#         return Response(
#             data=dict(
#                 status=True,
#                 message="Listings search completed successfully",
#                 data=listings_data,
#                 count=len(listings_data),
#             ),
#             status=status.HTTP_200_OK,
#         )


class BookingCreateAPIView(APIView):
    """Create a new booking for a listing"""

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Bookings"],
        description="Create a new booking for a rental listing. Validates availability and prevents double bookings.",
        request=CreateBookingSerializer,
        responses={
            201: inline_serializer(
                name="CreateBookingResponse",
                fields=dict(
                    status=serializers.BooleanField(),
                    message=serializers.CharField(),
                    data=BookingSerializer(),
                ),
            ),
        },
    )
    def post(self, request):
        """Create a new booking"""
        print("Request Data:", request.data)
        serializer = CreateBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        listing_id = serializer.validated_data.get("listing_id")
        check_in = serializer.validated_data.get("check_in")
        check_out = serializer.validated_data.get("check_out")
        user = serializer.validated_data.get("user")
        number_of_guests = serializer.validated_data.get("number_of_guests")

        booking_result = Booking.create_booking(
            listing_id=listing_id,
            user_id=user,
            check_in=check_in,
            check_out=check_out,
            number_of_guests=number_of_guests,
        )
        if not booking_result["status"]:
            return Response(
                data=dict(
                    status=False,
                    message=booking_result["message"],
                    data=None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            data=dict(
                status=True,
                message=booking_result["message"],
                # data=booking_result["booking"],
            ),
            status=status.HTTP_201_CREATED,
        )


# class UserBookingsAPIView(APIView):
#     """Fetch bookings for the authenticated user with optional filters"""

#     permission_classes = [IsAuthenticated]

#     @extend_schema(
#         tags=["Bookings"],
#         description="Fetch all bookings for the authenticated user with optional filters",
#         request=FetchBookingsSerializer,
#         responses={
#             200: inline_serializer(
#                 name="UserBookingsResponse",
#                 fields=dict(
#                     status=serializers.BooleanField(),
#                     message=serializers.CharField(),
#                     data=BookingSerializer(many=True),
#                     count=serializers.IntegerField(),
#                 ),
#             ),
#         },
#     )
#     def post(self, request):
#         """Fetch user's bookings with filters"""
#         serializer = FetchBookingsSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         filters = serializer.validated_data.get("filters", {})

#         # Build Q object for conditions
#         conditions = Q(user=request.user)

#         # Apply filters
#         listing_id = filters.get("listing_id")
#         if listing_id:
#             conditions.add(Q(listing_id=listing_id), Q.AND)

#         check_in = filters.get("check_in")
#         if check_in:
#             conditions.add(Q(check_in=check_in), Q.AND)

#         check_out = filters.get("check_out")
#         if check_out:
#             conditions.add(Q(check_out=check_out), Q.AND)

#         start_date = filters.get("start_date")
#         if start_date:
#             conditions.add(Q(created_at__gte=start_date), Q.AND)

#         end_date = filters.get("end_date")
#         if end_date:
#             conditions.add(Q(created_at__lte=end_date), Q.AND)

#         # Apply count limit
#         count = filters.get("count", 100)

#         # Fetch bookings using class method
#         bookings_data = Booking.fetch_bookings(
#             values=True, conditions=conditions, count=count
#         )

#         return Response(
#             data=dict(
#                 status=True,
#                 message="Bookings retrieved successfully",
#                 data=bookings_data,
#                 count=len(bookings_data),
#             ),
#             status=status.HTTP_200_OK,
#         )
