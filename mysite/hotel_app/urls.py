from .views import UserProfileViewSet, CountryListViewSet, CountryDetailViewSet, CityListViewSet, CityDetailViewSet, \
    AmenityViewSet, PropertyListViewSet, PropertyDetailViewSet, ImagePropertyViewSet, ReviewViewSet, FavoriteViewSet, \
    BookingListViewSet, BookingDetailViewSet, RegisterView, CustomLoginView, LogoutView
from rest_framework import routers
from django.urls import include, path



router = routers.DefaultRouter()

router.register(r'users', UserProfileViewSet, basename='user-profile')
router.register(r'amenities', AmenityViewSet, basename='amenity')
router.register(r'image_property', ImagePropertyViewSet, basename='image-property')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'favorite', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('country/', CountryListViewSet.as_view(), name='country-list'),
    path('country/<int:pk>/', CountryDetailViewSet.as_view(), name='country-detail'),

    path('city/', CityListViewSet.as_view(), name='city-list'),
    path('city/<int:pk>/', CityDetailViewSet.as_view(), name='city-detail'),

    path('properties/', PropertyListViewSet.as_view(), name='property-list'),
    path('properties/<int:pk>/', PropertyDetailViewSet.as_view(), name='property-detail'),

    path('booking/', BookingListViewSet.as_view(), name='booking-list'),
    path('booking/<int:pk>/', BookingDetailViewSet.as_view(), name='booking-detail')
]


