from django.contrib import admin
from products.models import Product, Price, Material, Tag, Image

# Register your models here.
admin.site.register(Product)
admin.site.register(Price)
admin.site.register(Material)
admin.site.register(Tag)
admin.site.register(Image)