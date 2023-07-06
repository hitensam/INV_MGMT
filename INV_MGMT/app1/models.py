import datetime
from django.db import models

# Create your models here.
class user(models.Model):
    user_email = models.CharField(max_length=50, primary_key=True)
    user_pass = models.CharField(max_length=60)
#ONLY FOR ADMIN STUFF


class customer(models.Model):
    customer_name = models.CharField(max_length=50, null=False)
    customer_phone = models.IntegerField(default=0, primary_key=True, unique=True)

    def __str__(self):
        return f'customer name : {self.customer_name}, customer_phone : {self.customer_phone}'
class stock(models.Model):
    item = models.CharField(max_length=50, null=False)
    width = models.FloatField(null=False)
    Roll_no = models.IntegerField(null=False)
    Net_wt = models.FloatField(null=False)
    Gr_wt = models.FloatField(null=False)
    sell = models.CharField(default='0', max_length=50)
    sell_no = models.IntegerField(default=0)

    def __str__(self):
        return f"item : {self.item}, width : {self.width}, Roll_no : {self.Roll_no}, Net_wt : {self.Net_wt}, \
            Gr_wt : {self.Gr_wt}, sell : {self.sell}, sell_no : {self.sell_no}"

class Sold(models.Model):
    customer_name = models.ForeignKey(customer, on_delete=models.CASCADE)
    item_purchase = models.ForeignKey(stock, on_delete=models.CASCADE)
    purchase_date = models.DateField() #datetime.date(2022, 9, 11)
    short_narration = models.CharField(max_length=50,default='', null=True)

    def __str__(self):
        return f'customer name : {self.customer_name}, item_purchase : {self.item_purchase}, purchase_date : {self.purchase_date}, short_narration = {self.short_narration}'




