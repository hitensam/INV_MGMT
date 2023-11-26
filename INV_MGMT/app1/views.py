from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, JsonResponse #Http404,HttpResponseNotFound, HttpResponseRedirect,
from . import  models #customer, Sold, stock
from django.db.models import Q
from . import IST_TIME as now
import csv
# import requests as req
# import emoji
import pandas as pd #added 23-05-23

from reportlab.platypus import *
from reportlab.lib.styles import *
from reportlab.lib import *
from reportlab.platypus import *
import math
import io
from reportlab.lib.units import inch

from wsgiref.util import FileWrapper#from django.core.servers.basehttp import FileWrapper #also using io and HttpResponse

from collections import defaultdict
def getMonthlyStats(request):
    if(request.method == "POST"):
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        try:
            obj = models.Sold.objects.filter(purchase_date__range=[start_date, end_date]).order_by('purchase_date').all()
        except:
            context = {"showForm": True, "heading": "Monthly Stats", 'message' : 'error, please retry.'}
            return render(request,'app1/getMonthlyStats.html', context=context)
        else:
            if len(obj) == 0:
                context = {"showForm": True, "heading": "Monthly Stats", 'message' : 'error, please retry.'}
                return render(request,'app1/getMonthlyStats.html', context=context)
            dates=[]
            weights = []
            for x in obj:
                dates.append(x.purchase_date)
                weights.append(x.item_purchase.Net_wt)
            # Dictionary to store total weights per month
            monthly_weights = defaultdict(float)

        # Iterate through dates and weights
            for date, weight in zip(dates, weights):
                month_key = date.strftime("%B %Y")
                monthly_weights[month_key] += weight

            # Separate lists for months and total weights
            months_list = []
            total_weights_list = []

            # Convert the defaultdict to lists
            for month, total_weight in monthly_weights.items():
                months_list.append(month)
                total_weights_list.append(total_weight)

            

            context = {"months": months_list, "weights": total_weights_list, "showForm": True, "heading": "Monthly Stats","duration": f'{months_list[0]} - {months_list[len(months_list) - 1]}'}
            return render(request,'app1/getMonthlyStats.html', context=context)

    else:
        obj = models.Sold.objects.filter(purchase_date__range=[now.six_months_ago(), now.today()]).order_by('purchase_date').all()
        if len(obj) == 0:
                context = {"showForm": True, "heading": "Monthly Stats", 'message' : 'No data from past 6 months.'}
                return render(request,'app1/getMonthlyStats.html', context=context)
        dates=[]
        weights = []
        for x in obj:
            dates.append(x.purchase_date)
            weights.append(x.item_purchase.Net_wt)
        # Dictionary to store total weights per month
        monthly_weights = defaultdict(float)

    # Iterate through dates and weights
        for date, weight in zip(dates, weights):
            month_key = date.strftime("%B %Y")
            monthly_weights[month_key] += weight

        # Separate lists for months and total weights
        months_list = []
        total_weights_list = []

        # Convert the defaultdict to lists
        for month, total_weight in monthly_weights.items():
            months_list.append(month)
            total_weights_list.append(total_weight)


        context = {"months": months_list, "weights": total_weights_list, "showForm": True, "heading": "Monthly Stats","duration": f'{months_list[0]} - {months_list[len(months_list) - 1]}'}
        return render(request,'app1/getMonthlyStats.html', context=context) 

def getDb(request):
    # Define the path to your db.sqlite3 file
    db_path = os.path.join(os.path.dirname(__file__), '/home/hitensam/INV_MGMT/db.sqlite3')

    # Open the file for reading
    db_file = open(db_path, 'rb')

    # Create a response with the file content
    response = HttpResponse(FileWrapper(db_file), content_type='application/x-sqlite3')
    response['Content-Disposition'] = 'attachment; filename=db.sqlite3'

    return response

def addcustomer(request):
    if (request.method == 'POST' ): #and 'user_logged' in request.session
        details = request.POST
        print('\n\n',details,'\n\n')
        try:
            models.customer.objects.filter(customer_name = str(details['cust_name'])).get()
            flag = 1
            # print('try working')
        except:
            flag = 0
        if (flag==1):
                context = {'heading': "Add Customer",'message' : 'Person with same name already exists.'}
                return render(request,'app1/addcustomer.html', context=context)
        try:
            models.customer.objects.filter(customer_phone = int(details['cust_mob'])).get()
            flag = 1
            # print('try working')
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
                            stock = addSoldStatus(models.stock.objects.all())
                            return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'NOTHING FOUND'}) if len(stock)==0 else render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'Stock Available & Sold', 'choice':details['choice']})
                        elif (details['choice'] == 'roll_no.'):
                            try:
                                stock = addSoldStatus(models.stock.objects.filter(Roll_no = int(details['query'])).all()) #.filter(Q(sell_no=0) & Q(sell='0'))
                                return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'NOTHING FOUND'}) if len(stock)==0 else render(request, 'app1/view.html', context={'stock' : stock, 'heading' : f'Stock: {(details["query"])}', 'choice':details['choice'], 'value':details['query']})
                            except:
                                return render(request, 'app1/view.html', context={'heading' : 'NOTHING FOUND'})
                        elif (details['choice'] == 'width'):
                            try:
                                stock = addSoldStatus(models.stock.objects.filter(width = float(details['query'])).all()) #.filter(Q(sell_no=0) & Q(sell='0'))
                                return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'NOTHING FOUND'}) if len(stock)==0 else render(request, 'app1/view.html', context={'stock' : stock, 'heading' : f'Stock: {(details["query"])}', 'choice':details['choice'], 'value':details['query']})
                            except:
                                return render(request, 'app1/view.html', context={'heading' : 'NOTHING FOUND'})
                        elif (details['choice'] == 'customer_number'):
                            stock = addSoldStatus(models.stock.objects.filter(sell_no__istartswith = int(details['query'])).all())
                            return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'NOTHING FOUND'}) if len(stock)==0 else render(request, 'app1/view.html', context={'stock' : stock, 'heading' :  f'Sales: {(details["query"])}','contentSetting' : True, 'choice':details['choice'], 'value':details['query']})
                        elif (details['choice'] == 'customer_name'):
                            try:
                                stock = addSoldStatus(models.stock.objects.filter(sell__icontains = str(details['query'])).all())
                                return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'NOTHING FOUND'}) if len(stock)==0 else render(request, 'app1/view.html', context={'stock' : stock, 'heading' : f'Sales: {(details["query"])}','contentSetting' : True, 'choice':details['choice'], 'value':details['query']})
                            except:
                                return render(request, 'app1/view.html', context={'heading' : 'NOTHING FOUND'})
                        elif (details['choice'] == 'item_name'):
                            stock = addSoldStatus(models.stock.objects.filter(item = (details['query'])).all()) #.filter(Q(sell_no=0) & Q(sell='0'))
                            return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'NOTHING FOUND'}) if len(stock)==0 else render(request, 'app1/view.html', context={'stock' : stock, 'heading' : f'Stock: {(details["query"])}', 'choice':details['choice'], 'value':details['query']})
                        else:
                            stock = addSoldStatus(models.stock.objects.all())
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
                stock = models.stock.objects.filter(sell ='0').all()[:5]
                return render(request, 'app1/view.html', context={'stock' : stock, 'heading' : 'Available Stock, Limited to 5.'})
        elif choice=='sold':
            if (request.method == 'POST'):
                    details=request.POST
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
                sold = models.Sold.objects.all().order_by('purchase_date')[:5]#Changed 01-06-2023
                if len(sold) == 0:
                    return render(request, 'app1/view.html', context={'sold' : sold, 'heading' : 'NOTHING FOUND'})
                return render(request, 'app1/view.html', context={'sold' : sold, 'heading' : 'Sold', 'showForm':'showForm'})


        else:
            return render(request, 'app1/view.html', context={'message' : 'Nothing to Show Here!'})

def addSoldStatus(stock):
    for x in stock:
        if(x.sell!="0" and x.sell_no!=0):
            soldDetails = models.Sold.objects.filter(item_purchase = x).get()
            x.sell = x.sell + f" on {modDate(soldDetails.purchase_date)} {soldDetails.short_narration} @ ₹{soldDetails.sell_price}/-"
            if(soldDetails.slitting_price!=0):
                x.sell = x.sell + f"slitting @ ₹{soldDetails.slitting_price}/-"
            if(soldDetails.pleating_price!=0):
                x.sell = x.sell + f"pleating @ ₹{soldDetails.pleating_price}/-"

    return stock;


def getProformaInvoice(request):
    if(request.method=="POST"):
        return HttpResponse("Nothing to show here.")

    else:
        context={'title' : "Proforma Invoice",'heading' : "Proforma Invoice", 'message':"", 'getProformaInvoice': True}
        return render(request,'app1/addsale.html', context=context)

def addSaleFromProformaID(request):
    if(request.method == "POST"):
        context={'heading' : "Add Sale from Proforma ID", 'addFromProformaID' : True}
        details = request.POST
        date = False; short_narration = False
        if ('sell_date' in details and len(details['sell_date']) != 0):
            date = details['sell_date']
        if ('short_narration' in details and len(details['short_narration']) != 0):
            short_narration = details['short_narration']
        PID = details['proforma_ID']
        if(len(PID)==0):
            context={'heading' : "Add Sale from Proforma ID", 'message':"Please enter the PID", 'addFromProformaID' : True}
            return render(request,'app1/view.html', context=context) 
        items = models.Proforma_Invoice.objects.filter(PID = PID).all()
        # print(items[0].item_req)
        if(len(items) == 0):
            context['message'] = "Nothing to show!!"
            return render(request,'app1/view.html', context=context)
        elif(items[0].PIDsold == True):
            context['message'] = "Already Sold!!"
            return render(request,'app1/view.html', context=context)
        
        elif(date!=False and short_narration!=False):
            customer = items[0].customer_name;
            for x in items:
                if(x.item_req.sell_no!=0 and x.item_req.sell!="0" and len(models.Sold.objects.filter(item_purchase = x.item_req).all()) != 0):
                    context['message'] = "Already Sold!!"
                    return render(request,'app1/view.html', context=context)
                x.item_req.sell_no = customer.customer_phone
                x.item_req.sell=customer.customer_name
                addToSold = models.Sold(customer_name = customer, item_purchase = x.item_req,
                                        purchase_date = date, short_narration=short_narration)
                if(x.total_non_tax_price!=0):
                    addToSold.sell_price = x.total_non_tax_price
                else:
                    addToSold.sell_price = x.sell_price
                if(x.igst!=0):
                    addToSold.igst=x.igst
                else:
                    addToSold.cgst=x.cgst
                    addToSold.sgst=x.sgst
                if(x.pleating_price!=0):
                    addToSold.pleating_price = x.pleating_price
                if(x.slitting_price!=0):
                    addToSold.slitting_price = x.slitting_price
                addToSold.packing_charges = x.packing_charges
                addToSold.save()
                x.item_req.save()
                x.PIDsold = True
                x.save()
            
            context['addedFromProformaID'] = True
            context['items'] = items
            context['info'] = items[0] 
            context['heading'] = f'Sales Added {customer.customer_name}'
            return render(request, 'app1/view.html', context=context)

        
        else:
            context['message'] = "PID exists."
            context['addedFromProformaID'] = True
            context['items'] = items
            context['info'] = items[0]            
            return render(request,'app1/view.html', context=context)


    else:
        context={'heading' : "Add Sale from Proforma ID", 'message':"Please enter the PID", 'addFromProformaID' : True}
        return render(request,'app1/view.html', context=context)

# def getOldPI(request):
#     if(request.method=="POST"):
#         details = request.POST
#         # PID = details[]
#         return HttpResponse("Hi")
#     else:
#         context={'heading' : "Add Sale from Proforma ID", 'message':"Please enter the PID", 'addFromProformaID' : True}
#         return render(request,'app1/view.html', context=context)
    
def addsale(request): #changed
    if(request.method=="POST"):
        details=request.POST
        print('\n\n', details, '\n\n')
        if('customer_phone' in details):
                sms_date_send=False;IGST=False;CGST = False;SGST = False;PACKING_CHARGES=False;PROFORMA_INVOICE = False;SALES_INVOICE=False;TOTAL_AMT=False; PROFORMA_INVOICE=False; RATE=False;click_count=False;PID=False;slitting_price = False; pleating_price = False
                if(details['slitting_price']!=""):
                    slitting_price = int(details['slitting_price'])
                if(details['pleating_price']!=""):
                    pleating_price = int(details['pleating_price'])
                if(details['IGST']!=""):
                    IGST=int(details['IGST'])
                if(details['CGST']!="" and details['SGST']!=""):
                    CGST=int(details['CGST'])
                    SGST=int(details['SGST'])
                if(details['PACKING_CHARGES']!=""):
                    PACKING_CHARGES = int(details['PACKING_CHARGES']);
                if(details['TOTAL_AMOUNT']!=""):
                    TOTAL_AMT = int(details['TOTAL_AMOUNT'])
                if(details['RATE']!=""):
                    RATE = int(details['RATE'])
                    TOTAL_AMT = False
                if('choice' in details and details['choice']=="PROFORMA_INVOICE"):
                    PROFORMA_INVOICE = True
                if('choice' in details and details['choice']=="SALES_INVOICE"):
                    SALES_INVOICE = True
                    PROFORMA_INVOICE = False
                if(details['click_count']!='0' and int(details['click_count'])>0):
                    click_count = int(details['click_count'])

                arrItems = [[details[f'item'],details[f'width'],details[f'Roll_no']]]
                if click_count:
                    arr = addedToArr(details, click_count)
                    arrItems=arrItems+arr

                roll=details['Roll_no'];
                try:
                    roll = int(roll)
                    multipleRoll=[roll]
                except:
                   multipleRoll= handleRoll(roll)
                arrItems[0][2] = multipleRoll;

        try:
                if(arrItems):
                    if (SALES_INVOICE or PROFORMA_INVOICE):
                        if(PROFORMA_INVOICE):
                            if ('sell_date' in details and len(details['sell_date']) != 0):
                                PID = now.getPid(str(details['sell_date']))
                            else:
                                PID = now.getPid(now.today())
                        df= [['S No.','Item','Width (MM)', 'Roll No.','Gross Weight (KG)', 'Net Weight (KG)']]
                        count=1
                        Net_Wt=0;Gr_Wt=0
                    PreviousAdded=False;
                    customer = models.customer.objects.filter(customer_phone = int(details['customer_phone'])).get()
                    showArr = []
                    for x in arrItems:
                        for y in x[2]:
                            stock = models.stock.objects.filter(Q(Roll_no = int(y)) & Q(item = x[0]) \
                        & Q(width =  x[1])).all()
                            showArr = showArr + list(stock)
                            stock = models.stock.objects.filter(Q(Roll_no = int(y)) & Q(item = x[0]) \
                        & Q(width =  x[1])).get()
                            if (SALES_INVOICE or PROFORMA_INVOICE):
                                if(PACKING_CHARGES==False):
                                        PACKING_CHARGES=0
                                if(IGST==False):
                                        IGST = 0;
                                if(SGST==False):
                                        SGST = 0;
                                if(CGST==False):
                                        CGST = 0
                                if(PROFORMA_INVOICE):
                                    if(TOTAL_AMT == False):
                                        TOTAL_AMT = 0
                                    elif(RATE == False):
                                        RATE = 0
                                    if ('sell_date' in details and len(details['sell_date']) != 0):
                                        date_set = str(details['sell_date'])
                                    else:
                                        date_set = now.today()
                                    addToProforma_Invoice = models.Proforma_Invoice(PID=PID,customer_name = customer, item_req = stock, req_date = date_set, \
                                                        total_non_tax_price = TOTAL_AMT,sell_price = RATE, packing_charges = PACKING_CHARGES)
                                    if(IGST!=0):
                                        addToProforma_Invoice.igst=IGST
                                    else:
                                        addToProforma_Invoice.cgst=CGST
                                        addToProforma_Invoice.sgst=SGST
                                    if(slitting_price):
                                        addToProforma_Invoice.slitting_price = slitting_price
                                    if(pleating_price):
                                        addToProforma_Invoice.pleating_price = pleating_price
                                    addToProforma_Invoice.save()
                                Net_Wt = Net_Wt +  stock.Net_wt; Gr_Wt = Gr_Wt + stock.Gr_wt;
                                arr =[count, stock.item,stock.width, stock.Roll_no, stock.Gr_wt, stock.Net_wt]
                                df.append(arr); count+=1
                            if(stock.sell!='0' and customer.customer_phone!=0):
                                return render(request,'app1/addsale.html', context={'heading' : "Add Sale",'message' :f'Previous Added: {PreviousAdded}, Roll: {stock.Roll_no} already sold.'})
                            if(not PROFORMA_INVOICE):
                                if ('sell_date' in details and len(details['sell_date']) != 0):
                                    sold = models.Sold(customer_name = customer, item_purchase = stock, purchase_date = str(details['sell_date']))
                                    sms_date_send = str(details['sell_date'])
                                    sold.save()
                                else:
                                    sold = models.Sold(customer_name = customer, item_purchase = stock, purchase_date = now.today())
                                    sms_date_send=now.today();
                                    sold.save()
                                if('short_narration' in details):
                                    sold.short_narration = str(details['short_narration'])
                                    sold.save()
                                if(TOTAL_AMT):
                                    sold.sell_price=TOTAL_AMT
                                elif(RATE):
                                    sold.sell_price=RATE
                                if(PACKING_CHARGES):
                                    sold.packing_charges = PACKING_CHARGES
                                if(IGST!=0):
                                    sold.igst=IGST
                                else:
                                    sold.cgst=CGST
                                    sold.sgst=SGST
                                if(slitting_price):
                                        sold.slitting_price = slitting_price
                                if(pleating_price):
                                        sold.pleating_price = pleating_price
                                sold.save()
                                stock.sell = customer.customer_name
                                stock.sell_no = customer.customer_phone
                                stock.save()
                            PreviousAdded="yes";

                    if (SALES_INVOICE or PROFORMA_INVOICE):
                        df.append(['','','','TOTAL',round(Gr_Wt,2),round(Net_Wt,2)])
                        if RATE:
                            TOTAL_AMT = round(Net_Wt,2) * RATE
                        else:
                            RATE = 0
                        if(pleating_price):
                            pleating_rate = pleating_price
                            pleating_price = round(Net_Wt, 2) * pleating_price
                        else:
                            pleating_price = 0
                            pleating_rate = pleating_price
                        if(slitting_price):
                            slitting_rate = slitting_price
                            slitting_price = round(Net_Wt, 2) * slitting_price
                        else:
                            slitting_price = 0
                            slitting_rate = slitting_price

                        df = add(df,PACKING_CHARGES,TOTAL_AMT,slitting_price,slitting_rate,pleating_price,pleating_rate,RATE, IGST,CGST,SGST)
                        

                        pg_data = df[1:]
                        if ( sms_date_send == False ) :
                            sms_date_send = now.today()
                        if(('sell_date' in details and len(details['sell_date']) != 0)):
                            sms_date_send = str(details['sell_date'])
                        sendDate = sms_date_send[8:10]+sms_date_send[4:8]+sms_date_send[0:4] #set from : 2023-07-22
                        return returnPDF(df,pg_data, customer.customer_name,PROFORMA_INVOICE,sendDate, PID)
                    return render(request, 'app1/view.html', context={'heading': f'Sales Added {customer.customer_name}', 'stock' : showArr})
        except:
                return render(request,'app1/addsale.html', context={'heading' : "Add Sale",'message' :'Fail, Exception Occurred'} )


    else:
        context={'heading' : "Add Sale", 'message':"", "addsale":True}
        GET=request.GET;
        if('param1' in GET):
            context['message']= GET['param1']
        return render(request,'app1/addsale.html', context=context)



def item_search(request):
    item = request.GET.get('item_search')
    width = request.GET.get('item_width')
    roll = request.GET.get('item_roll')
    multipleRoll=False
    try:
        roll = int(roll)
    except:
        multipleRoll = handleRoll(roll)
        roll = False
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
            if param=='return_alert_multiple':
                payload.append(response_data.item);
                payload.append(response_data.width);
                payload.append(response_data.Roll_no);



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
        search_data = models.customer.objects.filter(customer_name__icontains=party).all()
        addToPayload(search_data, param = 'party')

    if party_contact:
        search_data = models.customer.objects.filter(customer_name__iexact=party_contact).all()
        addToPayload(search_data, param = 'party_contact')

    if item and width and multipleRoll and return_alert:
        try:
            search_data = models.stock.objects.filter((Q(item = item) & Q(width= width) &Q(Roll_no = int(multipleRoll[0]) ))).get()
            sellStatus="AVAILABLE"
            totalNetWeight = 0
            totalGrossWeight=0
            strRoll = ""
            for x in multipleRoll:
                strRoll = strRoll+", "
                checkIfSold =  models.stock.objects.filter((Q(item = item) & Q(width= width) &Q(Roll_no = int(x)))).get()
                if(checkIfSold.sell_no!=0 and checkIfSold.sell!=0):
                    if(sellStatus=="AVAILABLE"):
                        sellStatus = "SOLD: "+str(checkIfSold.Roll_no)
                    else:
                        sellStatus =  sellStatus+" "+str(checkIfSold.Roll_no)
                    continue;
                totalNetWeight =  totalNetWeight + checkIfSold.Net_wt;
                totalGrossWeight =  totalGrossWeight + checkIfSold.Gr_wt
                strRoll = strRoll + f"{checkIfSold.Roll_no}"

            search_data.Roll_no = strRoll[2:]
            search_data.Gr_wt = totalGrossWeight;
            search_data.Net_wt = totalNetWeight;
            search_data.sell_no = sellStatus;
            search_data.sell = sellStatus
            send_data =[search_data.item,search_data.width,search_data.Roll_no, round(search_data.Net_wt,2), round(search_data.Gr_wt,2), search_data.sell,-1]
            return JsonResponse({'status' : 200, 'data' : send_data})

        except:
            return JsonResponse({'status' : 200, 'data':[]});

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

    return JsonResponse({'status' : 200, 'data' : payload})




def editData(request):
    if(request.method=='POST'):
        details = request.POST;
        print(details)
        try:
            #mods added to be added later :
            # try:
            #     roll = int(details['Roll_no'])
            #     multipleroll = [roll]
            # except:
            #     multipleroll = handleRoll(details['Roll_no'])

            # stock=[]
            # for x in multipleroll:
            #     stockObj = models.stock.objects.filter(Q(item=details['item']) & Q(width=details['width']) & Q(Roll_no=details['Roll_no'])).all()
            #     stock.append(stockObj)
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




def returnPDF(df, pg_data, customer_name,PROFORMA_INVOICE,DATE, PID):
    elements = []
    recs_pg = 39
    tot_pgs = math.ceil(len(pg_data) / recs_pg)

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate('sales.pdf', rightMargin=0, leftMargin=0, topMargin=0, bottomMargin=0)

    def createPageHeader():
        elements.append(Image('/home/hitensam/INV_MGMT/app1/static/app1/header.png', 7*inch, 1.7*inch)) #  ./app1/static/app1/header.png
        elements.append(Spacer(1, 10))
        if(PROFORMA_INVOICE):
            elements.append(Paragraph("Proforma Invoice", styles['Title']))
        else:
            elements.append(Paragraph("Sales Report", styles['Title']))
        elements.append(Spacer(1, 8))
        if customer_name:
            elements.append(Paragraph(f"Customer Name: {customer_name}", styles['Title']))
        if(DATE):
            elements.append(Spacer(1,8))
            elements.append(Paragraph(f"DATE: {DATE}"))
        if(PID):
            elements.append(Spacer(1,8))
            elements.append(Paragraph(f"ID: {PID}"))
        elements.append(Spacer(1,8))

    def paginateInventory(start, stop):
        tbl = Table(df[0:1] + pg_data[start:stop])
        tbl.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), '#F5F5F5'),
                                 ('FONTSIZE', (0, 0), (-1, 0), 8),
                                 ('GRID', (0, 0), (-1, -1), .5, '#a7a5a5')]))
        elements.append(tbl)
        elements.append(Spacer(1, 10))
        if (PROFORMA_INVOICE):
            elements.append(Image('/home/hitensam/INV_MGMT/app1/static/app1/footer.jpg', 7*inch, 0.5*inch)) #   ./app1/static/app1/footer.jpg



    def generatePDF():
        cur_pg = 0
        start_pos = 0
        stop_pos = recs_pg

        for cur_pg in range(tot_pgs):
            elements.clear()  # Clear the elements list before creating content for each page
            createPageHeader()
            paginateInventory(start_pos, stop_pos)
            elements.append(PageBreak())
            start_pos += recs_pg
            stop_pos += recs_pg

        doc.build(elements)
        file_path = "sales.pdf"  # Update the file path with the correct location
        if os.path.exists(file_path):
            with open(file_path, "rb") as pdf_file:
                pdf_content = pdf_file.read()

            response = FileResponse(io.BytesIO(pdf_content), content_type="application/pdf")
            if(PROFORMA_INVOICE):
                response["Content-Disposition"] = f"attachment; filename=PI.pdf"
                if(customer_name):
                    response["Content-Disposition"] = f"attachment; filename=PI-{customer_name}.pdf"
                return response
            response["Content-Disposition"] = f"attachment; filename=SALE.pdf"
            if(customer_name):
                response["Content-Disposition"] = f"attachment; filename=SALE-{customer_name}.pdf"
            return response
        else:
            return HttpResponse("File not found.")
    return generatePDF()

def getOldPdf(request):
    file_path = "sales.pdf"  # Update the file path with the correct location
    if os.path.exists(file_path):
            with open(file_path, "rb") as pdf_file:
                pdf_content = pdf_file.read()

            response = FileResponse(io.BytesIO(pdf_content), content_type="application/pdf")
            response["Content-Disposition"] = "attachment; filename=doc.pdf"
            return response
    else:
            return HttpResponse("File not found.")

def add(df,PACKING_CHARGES,TOTAL_AMT,SLITTING_CHARGES,SLITTING_RATE, PLEATING_CHARGES,PLEATING_RATE,RATE,IGST,CGST,SGST):
    if(TOTAL_AMT and (IGST or (CGST and SGST))):
        if(type(TOTAL_AMT)==str or type(IGST)==str or type(CGST)==str or type(SGST)==str):
            return df
        df.append(['','','','','',''])
        if RATE and RATE!=0:
            df.append(['','','','',f"TOTAL @ PRICE {RATE}/-",round(TOTAL_AMT,2)])
        else:
            df.append(['','','','',"TOTAL",round(TOTAL_AMT,2)])
        if(PACKING_CHARGES and PACKING_CHARGES!=0):
            df.append(['','','','',"PACKING CHARGES", round(PACKING_CHARGES,2)])
            TOTAL_AMT=TOTAL_AMT + PACKING_CHARGES;
        if(SLITTING_CHARGES!=False and SLITTING_CHARGES!=0):
             df.append(['','','','',f"SLITTING CHARGES @ {SLITTING_RATE}/-", round(SLITTING_CHARGES,2)])
             TOTAL_AMT = TOTAL_AMT + SLITTING_CHARGES
        if(PLEATING_CHARGES!=False and PLEATING_CHARGES!=0):
             df.append(['','','','',f"PLEATING CHARGES @ {PLEATING_RATE}/-", round(PLEATING_CHARGES,2)])
             TOTAL_AMT = TOTAL_AMT + PLEATING_CHARGES
        IGST_AMT = 0
        CGST_AMT = 0
        SGST_AMT = 0
        if(IGST and IGST!=0):
            IGST_AMT = TOTAL_AMT*(IGST/100);
            df.append(['','','','',f"IGST @ {IGST}%",round(IGST_AMT)])

        else:
            if(CGST and CGST!=0):
                CGST_AMT = TOTAL_AMT*(CGST/100);
                df.append(['','','','',f"CGST @ {CGST}%",round(CGST_AMT)])
            if(SGST and SGST!=0):
                SGST_AMT = TOTAL_AMT*(SGST/100);
                df.append(['','','','',f"SGST @ {SGST}%",round(SGST_AMT)])

        TOTAL_AMT = TOTAL_AMT+SGST_AMT+IGST_AMT + CGST_AMT;

        df.append(['','','','',"GRAND TOTAL",round(TOTAL_AMT)])

    return df;


def getQty(request):
    if (request.method=="POST"):
        click_count = False;RATE = False; PACKING_CHARGES = False; IGST = False; CGST = False; SGST = False; PROFORMA_INVOICE = True; customerName = False; TOTAL_AMT=False
        details=request.POST;
        # print(request.POST)
        arrItems = [[details[f'item'],details[f'width'],details[f'ntWeight']]]
        if(details['IGST']!=""):
            IGST=int(details['IGST'])
        if(details['CGST']!="" and details['SGST']!=""):
            CGST=int(details['CGST'])
            SGST=int(details['SGST'])
        if(details['PACKING_CHARGES']!=""):
            PACKING_CHARGES = int(details['PACKING_CHARGES']);
        if(details['TOTAL_AMOUNT']!=""):
            TOTAL_AMT = int(details['TOTAL_AMOUNT'])
        if(details['RATE']!=""):
            RATE = int(details['RATE'])
            TOTAL_AMT = False
        if('choice' in details and details['choice']=="PROFORMA_INVOICE"):
            PROFORMA_INVOICE = True
        if(details['click_count']!='0' and int(details['click_count'])>0):
                    click_count = int(details['click_count'])
        if click_count:
            arr = addedToArr(details, click_count)
            arrItems=arrItems+(arr)

        df= [['S No.','Item','Width (MM)', 'Roll No.','Gross Weight (KG)', 'Net Weight (KG)']]
        print(arrItems)

        Net_Wt=0; Gr_Wt=0;count=1
        for y in arrItems:
            itemNetWt=0
            item = y[0]
            width = y[1]
            targetWeight = y[2]
            targetWeight = float(targetWeight)
            stockObj = models.stock.objects.filter(item=item, width=width, sell=0, sell_no=0).all().order_by('-Net_wt')
            for x in stockObj:
                if(x.Net_wt<=targetWeight):
                    df.append([count, x.item,x.width, x.Roll_no, x.Gr_wt, x.Net_wt])
                    count+=1
                    targetWeight=targetWeight-x.Net_wt;
                    itemNetWt=itemNetWt + x.Net_wt
                    Gr_Wt=x.Gr_wt + Gr_Wt; Net_Wt=Net_Wt + x.Net_wt;

            df.append(["","","","","TOTAL",round(itemNetWt,2)]);
            df.append(["","","","","",""])

        df.append(['','','','TOTAL',round(Gr_Wt,2),round(Net_Wt,2)])
        if RATE:
            TOTAL_AMT = round(Net_Wt,2) * RATE
        df = add(df,PACKING_CHARGES,TOTAL_AMT,0,0,0,0,RATE, IGST,CGST,SGST)

        pg_data = df[1:]
        if('date' in details and len(details['date'])>0):
            sendDate = details['date']
        else:
            sendDate = now.today()
        sendDate = sendDate[8:10]+sendDate[4:8]+sendDate[0:4] #set from : 2023-07-22
        if('party_name' in details):
            customerName = details['party_name']
        return returnPDF(df,pg_data, customerName,PROFORMA_INVOICE,sendDate, False)


    else:
        return render(request,'app1/getQty.html', context={"heading": "Generate PI FROM WEIGHT",
                                                           "title": "Generate PI FROM WEIGHT"})

def handleRoll(roll):
    fetchNum=""
    multipleRoll=[]
    if(type(roll)==str):
        for y in roll:
            if(y == " "):
                if(len(fetchNum)!=0):
                    multipleRoll.append(fetchNum)
                fetchNum=""
                continue;
            else:
                fetchNum = fetchNum+y;
        if(len(fetchNum)!=0):
            multipleRoll.append(fetchNum)
    return multipleRoll


def addedToArr(details, click_count):
    arrItems=[]
    for x in range(1,click_count+1):
        if (f"Roll_no_{x}" in details):
            if(details[f"Roll_no_{x}"]!=""):
                try:
                    roll = int(details[f'Roll_no_{x}'])
                    multipleRoll = [roll]
                except:
                    roll = (details[f'Roll_no_{x}'])
                    multipleRoll= handleRoll(roll)
            else:
                multipleRoll=False
            item=False;width=False
            if(details[f'item_{x}']!=""):
                item=details[f'item_{x}'];
            if(details[f'width_{x}']!=""):
                width = details[f'width_{x}'];
            arrItems.append([item,width,multipleRoll])
        elif(f"ntWeight_{x}" in details):
            arrItems.append([details[f'item_{x}'],details[f'width_{x}'],details[f'ntWeight_{x}']])

    return arrItems;


def searchFilter(request):
    if(request.method=="POST"):
        details = request.POST;

        print(details)

        click_count = False; sell_date = False; customer_phone=False; item = False; width=False; Roll_no=False;
        if(details['item']!=''):
            item=details['item']
        if(details['width']!=''):
            width=details['width']
        if(details['Roll_no']!=''):
            Roll_no = details['Roll_no']
            try:
                Roll_no = [int(Roll_no)]
            except:
                Roll_no = handleRoll(Roll_no)
        arrItems = [[item, width, Roll_no]]
        if(details['click_count']!='' and int(details['click_count'])>0):
            click_count = int(details['click_count'])
            if click_count:
                    arr = addedToArr(details, click_count)
                    arrItems=arrItems+arr

        if(details['customer_phone']!='' ):
            customer_phone = details['customer_phone']

        # if(details['sell_date']!=""):
        #     sell_date=details['sell_date'];

        print("arrItems: ",arrItems)

        result = []
        for x in arrItems:
            if(x[0]!=False and x[1]==False and x[2]==False):
                if(customer_phone):
                    stock = addSoldStatus(models.stock.objects.filter(sell_no=customer_phone, item=x[0]))
                    stock = list(stock)
                    result = result+stock
                else:
                    stock = addSoldStatus(models.stock.objects.filter(item=x[0]))
                    stock = list(stock)
                    result = result+stock


            elif(x[1]!=False and x[0]==False and x[2]==False):
                if(customer_phone):
                    stock = addSoldStatus(models.stock.objects.filter(sell_no=customer_phone, width=x[1]))
                    stock = list(stock)
                    result = result+stock
                else:
                    stock = addSoldStatus(models.stock.objects.filter(width=x[1]))
                    stock = list(stock)
                    result = result+stock

            elif(x[2]!=False and x[0]==False and x[1]==False):
                for y in x[2]:
                    if(customer_phone):
                        stock = addSoldStatus(models.stock.objects.filter(sell_no=customer_phone, Roll_no=y))
                        stock = list(stock)
                        result = result+stock
                    else:
                        stock = addSoldStatus(models.stock.objects.filter(Roll_no=y))
                        stock = list(stock)
                        result = result+stock


            elif(x[0]!=False and x[1]!=False and x[2]==False):
                if(customer_phone):
                    stock = addSoldStatus(models.stock.objects.filter(sell_no=customer_phone, item=x[0],width=x[1]))
                    stock = list(stock)
                    result = result+stock
                else:
                    stock = addSoldStatus(models.stock.objects.filter(item=x[0],width=x[1]))
                    stock = list(stock)
                    result = result+stock

            elif(x[0]!=False and x[2]!=False and x[1]==False):
                for y in x[2]:
                    if(customer_phone):
                        stock = addSoldStatus(models.stock.objects.filter(sell_no=customer_phone, item=x[0],Roll_no=y))
                        stock = list(stock)
                        result = result+stock
                    else:
                        stock = addSoldStatus(models.stock.objects.filter(item=x[0],Roll_no=y))
                        stock = list(stock)
                        result = result+stock

            elif(x[0]==False and x[2]!=False and x[1]!=False):
                for y in x[2]:
                    if(customer_phone):
                        stock = addSoldStatus(models.stock.objects.filter(sell_no=customer_phone, width=x[1],Roll_no=y))
                        stock = list(stock)
                        result = result+stock
                    else:
                        stock = addSoldStatus(models.stock.objects.filter(width=x[1],Roll_no=y))
                        stock = list(stock)
                        result = result+stock


            elif(x[0]!=False and x[2]!=False and x[1]!=False):
                for y in x[2]:
                    if(customer_phone):
                        stock = addSoldStatus(models.stock.objects.filter(sell_no=customer_phone, item=x[0],width=x[1],Roll_no=y))
                        stock = list(stock)
                        result = result+stock
                    else:
                        stock = addSoldStatus(models.stock.objects.filter(item=x[0],width=x[1],Roll_no=y))
                        stock = list(stock)
                        result = result+stock
            elif(customer_phone and x[0]==False and x[2]==False and x[1]==False):
                stock = addSoldStatus(models.stock.objects.filter(sell_no=customer_phone))
                stock = list(stock)
                result = result+stock

        # return HttpResponse(details);
        return render(request, 'app1/view.html', context={'stock' : result, 'heading' : 'Search Results'})


    else:
        return render(request, 'app1/searchFilter.html', context={'heading': 'Search', 'title': 'Search'})


def modDate(sendDate):
    sendDate = str(sendDate)
    sendDate=sendDate[8:10]+sendDate[4:8]+sendDate[0:4]
    return sendDate
