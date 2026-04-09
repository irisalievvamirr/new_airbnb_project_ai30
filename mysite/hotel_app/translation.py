from .models import Country, City, Amenity
from modeltranslation.translator import TranslationOptions,register

@register(Country)
class ProductTranslationOptions(TranslationOptions):
    fields = ('country_name',)


@register(City)
class ProductTranslationOptions(TranslationOptions):
    fields = ('city_name',)


@register(Amenity)
class ProductTranslationOptions(TranslationOptions):
    fields = ('amenity_name',)
