from django.contrib import admin
from .models import Product, Customer, Repair, Invoice, ShopSettings

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Repair)
admin.site.register(Invoice)
admin.site.register(ShopSettings)
