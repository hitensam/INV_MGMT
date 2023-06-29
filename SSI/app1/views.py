# from email import message
# import re
from time import time
from django.shortcuts import render, redirect
from  django.http import HttpResponse, Http404,HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from .   import  models #customer, Sold, stock
from django.db.models import Q
from . import IST_TIME as now
import csv
import requests as req
import emoji
import pandas as pd #added 23-05-23
# import bcrypt
# Create your views here.

# def login(request):
#     if (request.method == 'POST'):
#             user_email = str(request.POST['user_email'])
#             user_pass = request.POST.get('user_pass');
#             print(f'/n/nuser_email = {user_email}')
#             try:
#                 models.user.objects.get(user_email=user_email)
#                 flag = 1
#             except:
#                 return render(request, 'app1/user.html',{'message' : 'user does not exists'})
#             if (flag):
#                 # print(f"{user.objects.get(user_email=user_email).user_pass}")
#                 if (bcrypt.checkpw(bytes(user_pass, 'utf-8'), bytes(models.user.objects.get(user_email=user_email).user_pass, 'utf-8'))):
#                     request.session['user_logged'] = user_email
#                     return redirect('/app1/view/stock')
#                 else:
#                     return render(request, 'app1/user.html',{'message' : 'Wrong password entered.'})
#     else:
#         if ('user_logged' in request.session):
#             return redirect('/app1/view/stock')
#         else:
#             return render(request, 'app1/user.html')

# def logout(request):
#     # if (request.method == 'POST'):
#     #     if (request.POST.get('logout')):
#     #         del request.session['user_logged']
#     #         return redirect('/app1/user/')

#     # else:
#     try:
#         # print("\n\n", request.POST.get('logout'),"\n\n")
#         del request.session['user_logged']
#         return redirect('/app1/login/')
#     except:
#         return redirect('/app1/login/')


# def error_404(request, exception):
#     return HttpResponseRedirect(reverse('view', args='stock'))

# def error_500(request, exception):
#     return HttpResponseRedirect(reverse('view', args='stock'))

def addcustomer(request):
    if (request.method == 'POST' ): #and 'user_logged' in request.session
        details = request.POST
        print('\n\n',details,'\n\n')
        try:
            models.customer.objects.filter(customer_name = str(details['cust_name'])).get()
            flag = 1
            print('try working')
        except:
            flag = 0
        if (flag==1):
                context = {'heading': "Add Customer",'message' : 'Person with same name already exists.'}
                return render(request,'app1/addcustomer.html', context=context)
        try:
            models.customer.objects.filter(customer_phone = int(details['cust_mob'])).get()
            flag = 1
            print('try working')
        except:
            flag = 0
        if (flag==1):
                context = {'heading': "Add Customer",'message' : 'Person with same number already exists.'}
                return render(request,'app1/addcustomer.html', context=context)
        else:
            try:
                obj = models.customer(customer_name = details['cust_name'], customer_phone = int(details['cust_mob']))
                obj.save()
                context = {'heading': "Add Customer",'message' : 'Details Saved'}
                return render(request,'app1/addcustomer.html', context=context)
            except:
                context = {'heading': "Add Customer",'message' : 'Please enter valid details'}
                return render(request,'app1/addcustomer.html', context=context)

    else:
        return render(request,'app1/addcustomer.html', context={'heading': "Add Customer"})


def addStock(request):
    if (request.method == 'POST'):
        details = request.POST
        print('\n\n', details, '\n\n')
        try:
            models.stock.objects.filter(Q(item = (details['item'])) & Q(Roll_no =  int(details['Roll_no']))\
                & Q(width =  int(details['width']))).get() #changes
            flag = 1
            # print('try working')
        except:
            flag = 0
        if (flag==1): #fixed on 26-05-23 but working same as earlier expected when if(flag):
            context = {'heading' : 'Add Stock','message' : 'Details exists already with same item and roll no.'}
            return render(request,'app1/addstock.html', context=context)
        else:
            obj = models.stock(item = details['item'], width = float(details['width']), Roll_no = int(details['Roll_no']), Net_wt = float(details['Net_wt']), Gr_wt = float(details['Gr_wt']))
            obj.save()
            return render(request, 'app1/addstock.html', context = {'heading' : 'Add Stock','message' : 'Stock Added'})
    else:
        return render(request, 'app1/addstock.html', context={'heading' : 'Add Stock'})


def view(request, choice=0):
        if choice=='customer':
            obj = models.customer.objects.all()
            return render(request, 'app1/view.html', context={'customer' : obj, 'heading' : 'Customers Data'})
        elif choice=='stock':
            if (request.method == 'POST'):
                details = request.POST
                print('\n\n', details, '\n\n')
                if ('choice' in details):
                        if (details['choice'] == 'available&sold'): #changed
                            stock = models.stock.objects.all()
                            return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'NOTHING FOUND'}) if len(stock)==0 else render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'Stock Available & Sold', 'choice':details['choice']})
                        elif (details['choice'] == 'roll_no.'):
                            try:
                                stock = models.stock.objects.filter(Roll_no = int(details['query'])).all() #.filter(Q(sell_no=0) & Q(sell='0'))
                                return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'NOTHING FOUND'}) if len(stock)==0 else render(request, 'app1/view.html', context={'stock' : stock, 'heading' : f'Stock: {(details["query"])}', 'choice':details['choice'], 'value':details['query']})
                            except:
                                return render(request, 'app1/view.html', context={'heading' : 'NOTHING FOUND'})
                        elif (details['choice'] == 'width'):
                            try:
                                stock = models.stock.objects.filter(width = float(details['query'])).all() #.filter(Q(sell_no=0) & Q(sell='0'))
                                return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'NOTHING FOUND'}) if len(stock)==0 else render(request, 'app1/view.html', context={'stock' : stock, 'heading' : f'Stock: {(details["query"])}', 'choice':details['choice'], 'value':details['query']})
                            except:
                                return render(request, 'app1/view.html', context={'heading' : 'NOTHING FOUND'})
                        elif (details['choice'] == 'customer_number'):
                            stock = models.stock.objects.filter(sell_no__istartswith = int(details['query'])).all()
                            return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'NOTHING FOUND'}) if len(stock)==0 else render(request, 'app1/view.html', context={'stock' : stock, 'heading' :  f'Sales: {(details["query"])}','contentSetting' : True, 'choice':details['choice'], 'value':details['query']})
                        elif (details['choice'] == 'customer_name'):
                            try:
                                stock = models.stock.objects.filter(sell__icontains = str(details['query'])).all()
                                return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'NOTHING FOUND'}) if len(stock)==0 else render(request, 'app1/view.html', context={'stock' : stock, 'heading' : f'Sales: {(details["query"])}','contentSetting' : True, 'choice':details['choice'], 'value':details['query']})
                            except:
                                return render(request, 'app1/view.html', context={'heading' : 'NOTHING FOUND'})
                        elif (details['choice'] == 'item_name'):
                            stock = models.stock.objects.filter(item = (details['query'])).all() #.filter(Q(sell_no=0) & Q(sell='0'))
                            return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'NOTHING FOUND'}) if len(stock)==0 else render(request, 'app1/view.html', context={'stock' : stock, 'heading' : f'Stock: {(details["query"])}', 'choice':details['choice'], 'value':details['query']})
                        else:
                            stock = models.stock.objects.all()
                            return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'Stock', 'message' : 'Invalid Choice.'})
                if ('itemName' in details):
                    customer = models.customer.objects.filter(customer_name = str(details['query'])).all()
                    if (len(customer)==1):
                        items = request.POST.getlist('itemName');
                        for x in items:
                            temp = x.split(',')
                            stock = models.stock.objects.filter( Q(item = temp[0]) & Q(Roll_no = int(temp[1])) & Q(width = (temp[2])) ).all()
                            if (len(stock)==1 and stock[0].sell=='0' and stock[0].sell_no==0):
                                sold = models.Sold(customer_name = customer[0], item_purchase = stock[0], purchase_date = now.today())
                                sold.save()
                                stock[0].sell = customer[0].customer_name
                                stock[0].sell_no = customer[0].customer_phone
                                stock[0].save()
                            else:
                                return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'STOCK', 'message' : 'invalid stock.'})
                        return render(request, 'app1/view.html', context={'heading' : 'CUSTOMER ISSUE'}) if len(customer)==0 else render(request, 'app1/view.html', context={'stock' : stock, 'heading' : f'Sales : {(details["query"])}','contentSetting' : True, 'choice':details['choice'], 'value':details['query']})

                    else:
                        return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'Stock', 'message' : 'Invalid Customer.'})

                else:
                    stock = models.stock.objects.all()
                    return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'STOCK', 'message' : 'Enter Valid Choice.'})
            else:
                stock = models.stock.objects.filter(sell ='0').all()
                return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'Available Stock'})
        elif choice=='sold':
            if (request.method == 'POST'):
                    details=request.POST
<<<<<<< Updated upstream
                    if('sell_date' in details and len(details['sell_date'])!=0): #'sell_date' in details can be removed.
                        if('choice' in details and details['choice']== 'range'):
                            sold=models.Sold.objects.filter(purchase_date__range=[str(details['sell_date']), now.today()]).all() #without .all() also same results. Checking Left.
                        else:
                            sold=models.Sold.objects.filter(purchase_date=str(details['sell_date'])).all()

                        if len(sold) == 0:
                            return render(request, 'app1/view.html', context={'sold' : sold, 'heading' : 'NOTHING FOUND', 'showForm':'showForm'})
                        return render(request, 'app1/view.html', context={'sold' : sold, 'heading' : 'Sold', 'showForm':'showForm'})
                    sold = models.Sold.objects.all().order_by('purchase_date')#Changed 01-06-2023
                    return render(request, 'app1/view.html', context={'sold' : sold, 'heading' : 'Sold', 'showForm':'showForm'})
            else:
                sold = models.Sold.objects.all().order_by('purchase_date')#Changed 01-06-2023
=======
                    if(str(details['sell_date'])):
                        sold=models.Sold.objects.filter(purchase_date=str(details['sell_date'])).all() #without .all() also same results. Checking Left.
                        if len(sold) == 0:
                            return render(request, 'app1/view.html', context={'sold' : sold, 'heading' : 'NOTHING FOUND'})
                        return render(request, 'app1/view.html', context={'sold' : sold, 'heading' : 'Sold'})
            else:
                sold = models.Sold.objects.all().order_by('purchase_date') #Changed 01-06-2023
>>>>>>> Stashed changes
                if len(sold) == 0:
                    return render(request, 'app1/view.html', context={'sold' : sold, 'heading' : 'NOTHING FOUND'})
                return render(request, 'app1/view.html', context={'sold' : sold, 'heading' : 'Sold', 'showForm':'showForm'})


        else:
            return render(request, 'app1/view.html', context={'message' : 'Nothing to Show Here!'})

def addsale(request): #changed
    details = request.POST
    print(request.POST)
    print('\n\n', details, '\n\n')
    # print(len(details['customer_phone']))
    # if (request.method == 'POST' and 'Roll_no' in details and 'item' in details and 'width' in details and len(details['customer_phone']) ==0):
    #     details = request.POST
    #     #
    #     try:
    #         stock = models.stock.objects.filter(Q(Roll_no = int(details['Roll_no'])) & Q(item = details['item']) \
    #             & Q(width =  int(details['width']))).get()
    #         return render(request,'app1/addsale.html', context={'heading' : "Add Sale",'message' : stock})
    #     except:
    #         return render(request,'app1/addsale.html', context={'heading' : "Add Sale",'message' :'Fail except (ADD SALE)'} )
    if(request.method == 'POST' and 'customer_phone' in details):
        details = request.POST

        #
        try:
        # if True:
            stock = models.stock.objects.filter(Q(Roll_no = int(details['Roll_no'])) & Q(item = details['item']) \
                & Q(width =  (details['width']))).get() #removed INT 01-06-2023
            customer = models.customer.objects.filter(customer_phone = int(details['customer_phone'])).get()
            print("\n\n", stock,'\n\n')
            print("\n\n", customer,'\n\n')
            print("\n\n", type(customer),'\n\n')
            if (stock.sell =='0' and stock.sell_no ==0 and customer.customer_phone !=0):
                print('\n\nentered\n\n')
                sms_date_send = 0 #added_later
                if ('sell_date' in details and len(details['sell_date']) != 0):
                    sold = models.Sold(customer_name = customer, item_purchase = stock, purchase_date = str(details['sell_date']))
                    sms_date_send = str(details['sell_date'])
                    sold.save()
                else:
                    sold = models.Sold(customer_name = customer, item_purchase = stock, purchase_date = now.today())
                    sms_date_send=now.today();
                    sold.save()
                print(sold)
                customer.customer_phone

                if('short_narration' in details):
                    sold.short_narration = str(details['short_narration'])
                    sold.save()

                stock.sell = customer.customer_name
                stock.sell_no = customer.customer_phone
                try:
                    smile_face = emoji.emojize(":grinning_face_with_big_eyes:")
                    message_var = f"Hi {customer.customer_name}!\n\nThanks for your purchase. {smile_face}\n\nItem: {details['item']} \nWidth: {(details['width'])}\nRoll No: {(details['Roll_no'])}\nDATED: {sms_date_send}"
                    api_key="api_key"
                    url = "https://www.fast2sms.com/dev/bulkV2"

                    querystring = {"authorization":api_key,"message": message_var,"language":"english","route":"q","numbers":customer.customer_phone}

                    headers = {
                        'cache-control': "no-cache"
                    }

                    response = req.request("GET", url, headers=headers, params=querystring)

                    print(response.text)
                except:
                    print("Message send failed.")
                stock.save()
                return render(request,'app1/addsale.html', context={'heading' : "Add Sale",'message' :'Sold Added'})
            else:
                return render(request,'app1/addsale.html', context={'heading' : "Add Sale",'message' :'Failed, Duplicate Sold'})
        except:
            return render(request,'app1/addsale.html', context={'heading' : "Add Sale",'message' :'Fail, Exception Occurred'} )


    else:
        context={'heading' : "Add Sale", 'message':""}
        GET=request.GET;
        if('param1' in GET):
            context['message']= GET['param1']
        return render(request,'app1/addsale.html', context=context)



def item_search(request):
    item = request.GET.get('item_search')
    width = request.GET.get('item_width')
    roll = request.GET.get('item_roll')
    party = request.GET.get('party_name')
    party_contact = request.GET.get('party_contact')
    return_alert = request.GET.get('return_alert')
    query = request.GET.get('query')
    general = request.GET.get('general')
    payload=[]
    def addToPayload(search_data, param):
        for response_data in search_data:
            if param=='width':
                payload.append(response_data.width)
            if param=='item':
                payload.append(response_data.item)
            if param=='roll':
                payload.append(response_data.Roll_no)
            if param=='party':
                payload.append(response_data.customer_name)
            if param=='party_contact':
                payload.append(response_data.customer_phone)
            if param=='return_alert':
                payload.append(response_data.item);
                payload.append(response_data.width);
                payload.append(response_data.Roll_no);
                payload.append(response_data.Net_wt);
                payload.append(response_data.Gr_wt);
                payload.append(response_data.sell);
                payload.append(response_data.sell_no);

    if general:
        search_in = ["""models.customer.objects.filter(customer_name__istartswith=general).all()""", \
             """models.stock.objects.filter(item__icontains = general).all()""",\
                """models.stock.objects.filter(width__range = (0,float(general))).all()""",\
                    """models.stock.objects.filter(Roll_no__range = (0,int(general))).all()"""]
        send_data = ['party', 'item', 'width', 'roll'] #
        for y in range(0,len(search_in)):
            search_data = eval(search_in[y])
            if len(search_data)!=0:
                addToPayload(search_data, param=send_data[y])
                break;
            else:
                continue;

    if party:
        search_data = models.customer.objects.filter(customer_name__istartswith=party).all()
        addToPayload(search_data, param = 'party')

    if party_contact:
        search_data = models.customer.objects.filter(customer_name__iexact=party_contact).all()
        addToPayload(search_data, param = 'party_contact')

    if item and width and roll and return_alert:
        search_data = models.stock.objects.filter((Q(item = item) & Q(width= width) &Q(Roll_no = int(roll) ))).all()
        addToPayload(search_data, param = 'return_alert')
    elif item and width and roll and query=='item-width-roll':
        search_data = models.stock.objects.filter((Q(item = item) & Q(width= width) &Q(Roll_no__range = (0,int(roll)) ))).filter(Q(sell_no = 0) & Q(sell = '0')).all()
        addToPayload(search_data, param = 'roll')

    elif item and width and query=='item-width':
        # print('working')
        search_data = models.stock.objects.filter(Q(item = item) & Q(width__range = (0,float(width)))).filter(Q(sell_no = 0) & Q(sell = '0')).all()
        addToPayload(search_data, param = 'width')
    elif(item and query=='item'):
        search_data = models.stock.objects.filter(item__icontains = item).filter(Q(sell_no = 0) & Q(sell = '0')).all()
        addToPayload(search_data, param = 'item')



    # print(payload)
    return JsonResponse({'status' : 200, 'data' : payload})




def editData(request):
    if(request.method=='POST'):
        details = request.POST;
        print(details)
        try:
            stock = models.stock.objects.filter(Q(item=details['item']) & Q(width=details['width']) & Q(Roll_no=details['Roll_no'])).all()
        except:
            stock=""
        try:
            customer = models.customer.objects.filter(customer_phone=details['customer_phone']).all()
        except:
            customer=""
        try:
            temp = models.Sold.objects.filter(Q(customer_name= customer[0]) & Q(item_purchase=stock[0])).all()
        except:
            temp=""
        if((len(details['sell_date'])!=0 or len(details['short_narration'])!=0) and len(temp)==1):
            edits=models.Sold.objects.filter(Q(customer_name=customer[0]) & Q(item_purchase=stock[0])).all()[0]
            if(len(details['sell_date'])!=0):
                edits.purchase_date = details['sell_date']
            if(len(details['short_narration'])!=0):
                edits.short_narration = details['short_narration']
            edits.save()
            return render (request,'app1/edit.html', context={'heading' : "Delete / Edit Data", 'message' : 'Edits Done'})

        elif len(stock)==1:
            if len(customer)==1:
                if (stock[0].sell_no == (customer[0].customer_phone)):
                    stock[0].sell_no = 0;
                    stock[0].sell = '0';
                    stock[0].save();
                    edits=models.Sold.objects.filter(Q(customer_name=customer[0]) & Q(item_purchase=stock[0])).all()[0]
                    edits.delete()
                    return render (request,'app1/edit.html', context={'heading' : "Delete / Edit Data", 'message' : 'Sale Deleted'})
                else:
                    return render (request,'app1/edit.html', context={'heading' : "Delete / Edit Data", 'message' : 'Please Enter Both Info To Delete Sell Correctly.'})
            else:
                temp = stock[0]
                temp1= models.Sold.objects.filter(item_purchase=temp).all() #added later
                if (temp.sell_no==0 and temp.sell=='0' and len(temp1)==0):
                    stock[0].delete()
                    return render (request,'app1/edit.html', context={'heading' : "Delete / Edit Data", 'message' : 'Product Deleted.'})
                else:
                    return render (request,'app1/edit.html', context={'heading' : "Delete / Edit Data", 'message' : 'Delete Sales First'})

        elif(len(customer)==1):
            edits=models.Sold.objects.filter(Q(customer_name=customer[0])).all()
            if (len(edits)==0):
                customer[0].delete()
                return render (request,'app1/edit.html', context={'heading' : "Delete / Edit Data", 'message' : 'Customer Deleted.'})
            else:
                return render (request,'app1/edit.html', context={'heading' : "Delete / Edit Data", 'message' : 'Please Delete Sales First.'})
        else:
            return render (request,'app1/edit.html', context={'heading' : "Delete / Edit Data", 'message' : 'FAIL'})
    else:
        return render (request,'app1/edit.html', context={'heading' : "Delete / Edit Data"})




def getfile(request,choice=0,value=0):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="backup_{now.fileDate()}.csv"'
    output = models.stock.objects.all()
    if(choice):
        if(choice=='roll_no.'):
            output = models.stock.objects.filter(Roll_no = int(value)).all()
            response['Content-Disposition'] = f'attachment; filename="Roll_no:_{value}_{now.fileDate()}.csv"'
        if(choice=='item_name'):
            output = models.stock.objects.filter(item = value).all()
            response['Content-Disposition'] = f'attachment; filename="Item:_{value}_{now.fileDate()}.csv"'
        if(choice=='width'):
            output = models.stock.objects.filter(width = int(value)).all()
            response['Content-Disposition'] = f'attachment; filename="Width:_{value}_{now.fileDate()}.csv"'
        if(choice=='customer_number'):
            output = models.stock.objects.filter(sell_no = int(value)).all()
            response['Content-Disposition'] = f'attachment; filename="CustomerNum:_{value}_{now.fileDate()}.csv"'
        if(choice=='customer_name'):
            output = models.stock.objects.filter(sell = (value)).all()
            response['Content-Disposition'] = f'attachment; filename="CustomerName:_{value}_{now.fileDate()}.csv"'
    writer = csv.writer(response)
    writer.writerow(['ITEM', 'WIDTH', 'ROLL NO.', 'NET WEIGHT', 'GROSS WEIGHT', 'SOLD PARTY', 'PARTY CONTACT', 'PURCHASE DATE'])
    for x in output:
        if(x.sell_no!=0):
            sold = models.Sold.objects.filter(item_purchase=x).get()
            writer.writerow([x.item,x.width,x.Roll_no,x.Net_wt,x.Gr_wt,x.sell,str(x.sell_no),sold.purchase_date])
        else:
            writer.writerow([x.item,x.width,x.Roll_no,x.Net_wt,x.Gr_wt,x.sell,str(x.sell_no)])
    return response


#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#item
#added on 25-05-2023 (fixed)
def restoreData(request):
    if request.method == 'POST' and 'csv_file' in request.FILES:
        file = request.FILES['csv_file']

        if not file.name.endswith('.csv'):
            return render(request, 'app1/restoreData.html', context={'heading': 'Restore Data', 'message': 'UPLOADED FILE IS NOT CSV'})
        else:
            try:
                context = {'heading': 'Restore Data', 'message': 'Results: ', 'stockAdded' :[], 'contactsAdded':[]}
                file = pd.read_csv(file, encoding='utf-8')
            except:
                return render(request, 'app1/restoreData.html', context={'heading': 'Restore Data', 'message': 'Encoding Issue'})
            l = file.values.tolist()
            for i in range(len(l)):
                if(len(l[i])==2):
                    try:
                        l[i][0] = str(l[i][0]);
                        l[i][1] = int(l[i][1])
                        if(l[i][1]!=0 and len(str(l[i][1]))!=10):
                                context['heading'] = f'Customer num {i+1} less than 10 digits'
                                context['message'] = context['message'] + f'\\n{i+1} error'
                                return render(request, 'app1/restoreData.html', context=context)
                        existingCustomer = models.customer.objects.filter(Q(customer_name=(l[i][0]))|Q(customer_phone=int(l[i][1])))
                        if not existingCustomer:
                                    existingCustomer = models.customer(customer_name=l[i][0], customer_phone=l[i][1])
                                    existingCustomer.save()
                                    context['message'] = context['message'] + f'\\n{i+1} added'
                                    context['contactsAdded'].append(existingCustomer)

                        else:
                            context['message'] = context['message'] + f'\\n{i+1} already exists'

                    except:
                        context['heading'] = f'Customer details {i+1} issue.'
                        context['message'] = context['message'] + f'\\n{i+1} error'
                        return render(request, 'app1/restoreData.html', context=context)

                else:
                # print('Name : ', l[i][0], " ", 'width ', l[i][1], " ", 'roll : ', l[i][2], " net :", l[i][3], " gross : ", l[i][4])
                    try:
                        try:
                            # str(l[i][0])#item
                            # float(l[i][1])#width
                            # int(l[i][2])#roll
                            # float(l[i][3])#Net_wt
                            # float(l[i][4])#Gr_wt
                            models.stock.objects.filter(item=l[i][0], width=(l[i][1]), Roll_no=(l[i][2]), Net_wt=(l[i][3]), Gr_wt=(l[i][4]))
                        except:
                            context['message'] = context['message'] + f'\\n{i+1} stock error '
                            context['heading'] = f'Stock {i+1} details error'
                            return render(request, 'app1/restoreData.html', context=context)
                        stock = models.stock.objects.filter(item=l[i][0], width=float(l[i][1]), Roll_no=int(l[i][2]), Net_wt=float(l[i][3]), Gr_wt=float(l[i][4])).get()
                        context['message'] = context['message'] + f'\\n{i+1} exists '
                    except models.stock.DoesNotExist:
                        stock = models.stock(item=l[i][0], width=float(l[i][1]), Roll_no=int(l[i][2]), Net_wt=float(l[i][3]), Gr_wt=float(l[i][4]))
                        stock.save()
                        context['stockAdded'].append(stock)
                        context['message'] = context['message'] + f'\\n{i+1} added '
                    if (len(l[i])==8):
                        try:
                                l[i][6] = int(l[i][6])
                                l[i][7]=str(l[i][7])
                                l[i][7] = l[i][7][6:10]+l[i][7][2:6]+l[i][7][0:2]
                                if(l[i][6]!=0 and len(str(l[i][6]))!=10):
                                    context['heading'] = f'Customer num {i+1} less than 10 digits'
                                    context['message'] = context['message'] + f'\\n{i+1} error'
                                    return render(request, 'app1/restoreData.html', context=context)
                        except:
                                context['heading'] = f'Customer num/date {i+1} error'
                                context['message'] = context['message'] + f'\\n{i+1} error'
                                return render(request, 'app1/restoreData.html', context=context)
                        if str(l[i][5]) != '0' and l[i][6] != 0 and l[i][7] != '':
                                existingCustomer = models.customer.objects.filter(Q(customer_name=(l[i][0]))|Q(customer_phone=int(l[i][1])))#updated condition
                                if not existingCustomer:
                                        existingCustomer = models.customer(customer_name=l[i][5], customer_phone=l[i][6])
                                        existingCustomer.save()
                                else:
                                    existingCustomer=existingCustomer.get()
                                try:
                                        sold = models.Sold.objects.filter(item_purchase=stock).get()
                                        context['heading'] = f'Sold exists {i+1} error'
                                        context['message'] = context['message'] + f'\\n{i+1} duplicate sold error'
                                        return render(request, 'app1/restoreData.html', context=context)
                                except models.Sold.DoesNotExist:
                                    # context['message'] = context['message'] + f'models.Sold'
                                    try:
                                                # context['message'] = context['message'] + f'entered try'
                                                sold = models.Sold(customer_name=existingCustomer, item_purchase=stock, purchase_date=(l[i][7]))

                                                sold.save()
                                                stock.sell = existingCustomer.customer_name
                                                stock.sell_no = existingCustomer.customer_phone
                                                stock.save()
                                                context['message'] = context['message'] + f'sold added'
                                    except:
                                                context['heading'] = f"DATE NOT IN DD-MM-YYYY Format: {i+1}"
                                                return render(request, 'app1/restoreData.html', context=context)
        if(len(context['contactsAdded'])!=0 and len(context['stockAdded'])!=0):
            return render(request, 'app1/restoreData.html', context=context)

        if(len(context['contactsAdded'])!=0):
            customer=context['contactsAdded']
            message=context['message']
            return render(request, 'app1/view.html', context={'customer' : customer, 'heading' : 'Customers Added','message': message})

        if(len(context['stockAdded'])!=0):
            stock=context['stockAdded']
            message=context['message']
            return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'Stock Added', 'message': message,'restoreData':'restoreData'})

        return render(request, 'app1/restoreData.html', context=context)
    else:
        context={'heading' : "Restore Data", 'message':"UPLOAD CSV FILE ONLY."}
        return render(request, 'app1/restoreData.html', context=context)

def getInfo(request): #item,width,rollNo=0 removed
    if(request.method=="GET"):
        context={'heading':'Info/Add Sale', 'message':''}
        GET=request.GET;
        if('item' in GET and 'width' in GET and 'RollNo' in GET ):
            item=GET['item']
            width=GET['width']
            rollNo=GET['RollNo']
            try:
                findStock = models.stock.objects.filter(item=item, width=width, Roll_no=rollNo).get()
                context.update({'findStock' : findStock})
                if (findStock.sell=="0" and findStock.sell_no==0):
                        return render(request,'app1/getInfo.html', context=context)
                else:
                    findSoldStock = models.Sold.objects.filter(item_purchase=findStock).get()
                    context.update({'findSoldStock' : findSoldStock})
                    context['message'] = "Already Sold."
                    return render(request,'app1/getInfo.html', context=context)

            except:
                context['message'] = "Stock with given info does not exist."
                return redirect('/addSale/?param1={}'.format(context['message']))

        else:
            return redirect('/addSale/?param1={}'.format('All Parameters Not Specified.'))


    else:
        return redirect('/addSale/?param1={}'.format('Invalid URL'))