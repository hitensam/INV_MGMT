from django.contrib import admin
from .models import Sold, stock, customer, user
# Register your models here.

admin.site.register(Sold)
admin.site.register(stock)
admin.site.register(customer)
admin.site.register(user)



