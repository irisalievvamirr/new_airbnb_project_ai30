from rest_framework import serializers
from .models import UserProfile, Country, City, Amenity, Property, ImageProperty, Review, Favorite, BookingProperty
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'role', 'avatar']


class CountryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name', 'country_image']

class CityListSerializers(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name', 'city_image']

class AmenitySerializers(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'amenity_name']

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'property', 'user', 'rating', 'comment', 'created_at']

class PropertyListSerializers(serializers.ModelSerializer):
    city = CityListSerializers()
    get_avg_rating = serializers.SerializerMethodField()
    get_count_reviews = serializers.SerializerMethodField()
    class Meta:
        model = Property
        fields = ['id', 'prop_name', 'prop_image', 'city', 'prop_type', 'price_per_night', 'get_avg_rating', 'get_count_reviews']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_reviews(self, obj):
        return obj.get_count_reviews()

class CityDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name', 'city_image']

class CountryDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name', 'country_image']

class ImagePropertySerializers(serializers.ModelSerializer):
    class Meta:
        model = ImageProperty
        fields = ['id', 'image']

class FavoriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

class BookingListPropertySerializers(serializers.ModelSerializer):
    class Meta:
        model = BookingProperty
        fields = ['id', 'guest', 'property', 'booking_status']

class BookingDetailPropertySerializers(serializers.ModelSerializer):
    class Meta:
        model = BookingProperty
        fields = ['id', 'guest', 'property', 'guest_count', 'check_in_date', 'check_out_date', 'booking_status', 'created_at']

class PropertyDetailSerializers(serializers.ModelSerializer):
    city = CityListSerializers()
    country = CountryListSerializers()
    owner = UserProfileSerializers()
    amenity = AmenitySerializers(many=True)
    reviews = ReviewSerializers(read_only=True, many=True)
    get_avg_rating = serializers.SerializerMethodField()
    get_count_reviews = serializers.SerializerMethodField()
    images_prop = ImagePropertySerializers(read_only=True, many=True)
    class Meta:
        model = Property
        fields = ['id', 'prop_name', 'prop_image', 'description', 'price_per_night', 'address', 'country', 'city', 'is_active', 'prop_type', 'prop_rules', 'max_guests', 'bedrooms', 'bathrooms', 'amenity', 'owner', 'reviews', 'get_avg_rating', 'get_count_reviews', 'images_prop']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_reviews(self, obj):
        return obj.get_count_reviews()