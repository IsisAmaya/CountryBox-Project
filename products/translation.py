from modeltranslation.translator import translator, TranslationOptions
from .models import Product

class ProductTranslationOptions(TranslationOptions):
    fields = ('description', 'country', 'size')

translator.register(Product, ProductTranslationOptions)
