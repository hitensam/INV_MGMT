from django.contrib import admin
from .models import Sold, stock, customer, user, Proforma_Invoice
# Register your models here.

admin.site.register(Sold)
admin.site.register(stock)
admin.site.register(customer)
admin.site.register(user)
admin.site.register(Proforma_Invoice)



