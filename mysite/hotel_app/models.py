from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLE = (
('host', 'host'),
('guest', 'guest')
)

class UserProfile(AbstractUser):
    role = models.CharField(max_length=10, choices=USER_ROLE, null=True, blank=True)
    phone_number = PhoneNumberField(region='KG', default='+996')
    avatar = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return f'{self.username}: {self.role}'

class Country(models.Model):
    country_name = models.CharField(max_length=32)
    country_image = models.ImageField(upload_to='country_images/')

    def __str__(self):
        return self.country_name

class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    city_name = models.CharField(max_length=32)
    city_image = models.ImageField(upload_to='city_images/')

    def __str__(self):
        return f'{self.country}: {self.city_name}'

class Amenity(models.Model):
    amenity_name = models.CharField(max_length=32)
    amenity_image = models.ImageField(upload_to='amenity_images/')

    def __str__(self):
        return self.amenity_name

class Property(models.Model):
    host = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='properties')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='prop_country')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='prop_city')
    prop_name = models.CharField(max_length=255)
    prop_image = models.ImageField(upload_to='prop_images/')
    address = models.CharField(max_length=50)
    amenity = models.ManyToManyField(Amenity)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    description = models.TextField()
    price_per_night = models.PositiveSmallIntegerField(default=0)
    PROP_TYPE = (
    ('Apartment', 'Apartment'),
    ('House', 'House'),
    ('Studio', 'Studio'),
    ('Villa', 'Villa'),
    ('Penthouse', 'Penthouse')
    )
    prop_type = models.CharField(max_length=10, choices=PROP_TYPE)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    PROP_RULES = (
    ('No smoking', 'No smoking'),
    ('Pets allowed', 'Pets allowed'),
    ('There is a safe', 'There is a safe'),
    ('Cleanliness and order', 'Cleanliness and order'),
    ('Careful attitude to property', 'Careful attitude to property'),
    ('Observance of silence', 'Observance of silence')
    )
    prop_rules = models.CharField(max_length=32, choices=PROP_RULES, null=True, blank=True)
    max_guests = models.PositiveSmallIntegerField(default=0)
    bedrooms = models.PositiveSmallIntegerField(default=0)
    bathrooms = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.city}: {self.prop_name}'

    def get_avg_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return sum([i.rating for i in reviews]) / reviews.count()
        return 0

    def get_count_reviews(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return reviews.count()
        return 0

class ImageProperty(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images_prop')
    image = models.ImageField(upload_to='images_prop/')

class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField(null=True, blank=True)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.property} | {self.rating}'

class Favorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Property, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

class BookingProperty(models.Model):
    guest = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    BOOKING_STATUS = (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
    ('Cancelled', 'Cancelled')
    )
    booking_status = models.CharField(max_length=10, choices=BOOKING_STATUS, default='Pending')
    guest_count = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"Бронь на {self.property.prop_name} от {self.guest.username}"
