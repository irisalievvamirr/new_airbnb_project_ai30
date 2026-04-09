from django_filters.rest_framework import FilterSet
from .models import Property

class PropertyFilter(FilterSet):
    class Meta:
        model = Property
        fields = {
            'city': ['exact'],
            'prop_type': ['exact'],
            'max_guests': ['exact'],
            'price_per_night': ['gt', 'lt'],
            'amenity': ['exact'],
        }