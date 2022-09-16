from email import message
import re
from time import time
from django.shortcuts import render, redirect
from  django.http import HttpResponse, Http404,HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from .   import  models #customer, Sold, stock
from django.db.models import Q
from . import IST_TIME as now
import bcrypt
# Create your views here.

def login(request):
    if (request.method == 'POST'):
            user_email = str(request.POST['user_email'])
            user_pass = request.POST.get('user_pass'); 
            print(f'/n/nuser_email = {user_email}')
            try:
                models.user.objects.get(user_email=user_email)
                flag = 1
            except:
                return render(request, 'app1/user.html',{'message' : 'user does not exists'})
            if (flag):
                # print(f"{user.objects.get(user_email=user_email).user_pass}")
                if (bcrypt.checkpw(bytes(user_pass, 'utf-8'), bytes(models.user.objects.get(user_email=user_email).user_pass, 'utf-8'))):
                    request.session['user_logged'] = user_email
                    return redirect('/app1/view/stock')
                else:
                    return render(request, 'app1/user.html',{'message' : 'Wrong password entered.'})
    else:
        if ('user_logged' in request.session):
            return redirect('/app1/view/stock')
        else:    
            return render(request, 'app1/user.html')

def logout(request):
    # if (request.method == 'POST'):
    #     if (request.POST.get('logout')):
    #         del request.session['user_logged']
    #         return redirect('/app1/user/')

    # else:
    try:
        # print("\n\n", request.POST.get('logout'),"\n\n")
        del request.session['user_logged']
        return redirect('/app1/login/')
    except:
        return redirect('/app1/login/')

def addcustomer(request):
    if (request.method == 'POST' and 'user_logged' in request.session):
        details = request.POST
        print('\n\n',details,'\n\n')
        try:
            models.customer.objects.filter(customer_phone = int(details['cust_mob'])).get()
            flag = 1
            print('try working')
        except:
            flag = 0
        if (flag):
                context = {'message' : 'Details exists already'}
                return render(request,'app1/customer.html', context=context)
        else:
            try:    
                obj = models.customer(customer_name = details['cust_name'], customer_phone = int(details['cust_mob']))
                obj.save()
                context = {'message' : 'Details Saved'}
                return render(request,'app1/customer.html', context=context)
            except:
                context = {'message' : 'Please enter valid details'}
                return render(request,'app1/customer.html', context=context)

    else:
        return render(request,'app1/customer.html')


def addStock(request):
    if (request.method == 'POST' and 'user_logged' in request.session):
        details = request.POST
        print('\n\n', details, '\n\n')
        try:
            models.stock.objects.filter(Q(item = (details['item'])) & Q(Roll_no =  int(details['Roll_no']))\
                & Q(width =  int(details['width']))).get() #changes
            flag = 1
            print('try working')
        except:
            flag = 0
        if (flag):
            context = {'message' : 'Details exists already with same item and roll no.'}
            return render(request,'app1/stock.html', context=context)
        else:
            obj = models.stock(item = details['item'], width = float(details['width']), Roll_no = int(details['Roll_no']), Net_wt = float(details['Net_wt']), Gr_wt = float(details['Gr_wt']))
            obj.save()
            return render(request, 'app1/stock.html', context = {'message' : 'stock added'})
    else:
        return render(request, 'app1/stock.html', context={'message' : ''})


def view(request, choice=0):
    if ('user_logged' in request.session):
        if choice=='customer':
            obj = models.customer.objects.all()
            return render(request, 'app1/view.html', context={'customer' : obj, 'heading' : 'CUSTOMERS'})
        elif choice=='stock':
            if (request.method == 'POST'):
                details = request.POST
                print('\n\n', details, '\n\n')
                if ('choice' in details):
                        if (details['choice'] == 'available&sold'): #changed
                            stock = models.stock.objects.all()
                            return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'NOTHING FOUND'}) if len(stock)==0 else render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'STOCK AVAILABLE & SOLD'})
                        elif (details['choice'] == 'roll_no.'):
                            try:
                                stock = models.stock.objects.filter(Roll_no = int(details['query'])).all()
                                return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'NOTHING FOUND'}) if len(stock)==0 else render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'STOCK'})
                            except:
                                return render(request, 'app1/view.html', context={'heading' : 'NOTHING FOUND'})
                        elif (details['choice'] == 'width'):
                            try:
                                stock = models.stock.objects.filter(width = float(details['query'])).all()
                                return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'NOTHING FOUND'}) if len(stock)==0 else render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'STOCK'})
                            except:
                                return render(request, 'app1/view.html', context={'heading' : 'NOTHING FOUND'})
                        elif (details['choice'] == 'sold'):
                            stock = models.stock.objects.filter(sell = (details['query'])).all()
                            return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'NOTHING FOUND'}) if len(stock)==0 else render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'STOCK'})
                        elif (details['choice'] == 'customer_no'):
                            try:
                                stock = models.stock.objects.filter(sell_no = int(details['query'])).all()
                                return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'NOTHING FOUND'}) if len(stock)==0 else render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'STOCK'})
                            except:
                                return render(request, 'app1/view.html', context={'heading' : 'NOTHING FOUND'})
                        elif (details['choice'] == 'item_name'):
                            stock = models.stock.objects.filter(item = (details['query'])).all()
                            return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'NOTHING FOUND'}) if len(stock)==0 else render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'STOCK'})
                        else:
                            stock = models.stock.objects.all()
                            return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'STOCK', 'message' : 'invalid choice.'})
                else:
                    stock = models.stock.objects.all()
                    return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'STOCK', 'message' : 'enter valid choice.'})
            else:    
                stock = models.stock.objects.filter(sell ='0').all()
                return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'AVAILABLE STOCK'})
        elif choice=='sold':
            sold = models.Sold.objects.all()
            if len(sold) == 0:
                return render(request, 'app1/view.html', context={'sold' : sold, 'heading' : 'NOTHING FOUND'})
            return render(request, 'app1/view.html', context={'sold' : sold, 'heading' : 'SOLD'})

    
    else:
        return render(request, 'app1/view.html', context={'message' : 'nothing to show'})
        
def sell(request): #changed
    details = request.POST
    print('\n\n', details, '\n\n') 
    # print(len(details['customer_phone']))
    if ('user_logged' in request.session and request.method == 'POST' and 'Roll_no' in details and 'item' in details and 'width' in details and len(details['customer_phone']) ==0):
        details = request.POST
        #
        try:
            stock = models.stock.objects.filter(Q(Roll_no = int(details['Roll_no'])) & Q(item = details['item']) \
                & Q(width =  int(details['width']))).get()
            return render(request,'app1/sell.html', context={'message' : stock})
        except:
            return render(request,'app1/sell.html', context={'message' :'fail except'} )
    elif(request.method == 'POST' and 'customer_phone' in details):
        details = request.POST
        #
        try:
            stock = models.stock.objects.filter(Q(Roll_no = int(details['Roll_no'])) & Q(item = details['item']) \
                & Q(width =  int(details['width']))).get()
            customer = models.customer.objects.filter(customer_phone = int(details['customer_phone'])).get()
            print("\n\n", stock,'\n\n')
            print("\n\n", customer,'\n\n')
            print("\n\n", type(customer),'\n\n')
            if (stock.sell =='0' and stock.sell_no ==0 and customer.customer_phone !=0):
                print('\n\nentered\n\n')
                sold = models.Sold(customer_name = customer, item_purchase = stock, purchase_date = now.today())
                sold.save()
                print(sold)
                stock.sell = customer.customer_name
                stock.sell_no = customer.customer_phone
                stock.save()
                return render(request,'app1/sell.html', context={'message' :'sold added'})
            else:
                return render(request,'app1/sell.html', context={'message' :'failed duplicate sold'})
        except:
            return render(request,'app1/sell.html', context={'message' :'fail except'} )


    else:
        return render(request,'app1/sell.html')