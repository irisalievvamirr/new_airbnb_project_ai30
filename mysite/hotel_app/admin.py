from django.contrib import admin
from .models import UserProfile, Country, City, Amenity, Property, ImageProperty, Review, Favorite, BookingProperty

from modeltranslation.admin import TranslationAdmin

@admin.register(Country, City, Amenity)
class AllAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class ImagePropertyInline(admin.TabularInline):
    model = ImageProperty
    extra = 1

admin.site.register(UserProfile)
admin.site.register(Property)
admin.site.register(Review)
admin.site.register(Favorite)
admin.site.register(BookingProperty)


