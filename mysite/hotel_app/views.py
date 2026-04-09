from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import UserProfileSerializers, CountryListSerializers, CountryDetailSerializers, CityListSerializers, CityDetailSerializers, AmenitySerializers, PropertyListSerializers, PropertyDetailSerializers, ImagePropertySerializers, ReviewSerializers, FavoriteSerializers, BookingListPropertySerializers, BookingDetailPropertySerializers, RegisterSerializer, LoginSerializer
from .models import UserProfile, Country, City, Amenity, Property, ImageProperty, Review, Favorite, BookingProperty
from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PropertyFilter
from .pagination import PropertyPagination
from .permissions import IsHostUser, HostCheck

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CountryListViewSet(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryListSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CountryDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryDetailSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CityListViewSet(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CityListSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CityDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CityDetailSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AmenityViewSet(viewsets.ModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PropertyListViewSet(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyListSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['city', 'prop_type', 'amenity', 'price_per_night', 'max_guests', 'prop_name', 'description']
    ordering_fields = ['price_per_night', 'created_at']
    filterset_class = PropertyFilter
    pagination_class = PropertyPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsHostUser]

class PropertyDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyDetailSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, HostCheck]

class ImagePropertyViewSet(viewsets.ModelViewSet):
    queryset = ImageProperty.objects.all()
    serializer_class = ImagePropertySerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookingListViewSet(generics.ListCreateAPIView):
    queryset = BookingProperty.objects.all()
    serializer_class = BookingListPropertySerializers
    permission_classes = [permissions.IsAuthenticated]

class BookingDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookingProperty.objects.all()
    serializer_class = BookingDetailPropertySerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



