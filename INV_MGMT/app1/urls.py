from django.urls import path
from . import views
from django.views.generic import RedirectView


app_name = 'app1'

urlpatterns = [
    path('', RedirectView.as_view(url='searchFilter')),
    path("addCustomer/", views.addcustomer, name='addcustomer'),
    path('addStock/', views.addStock, name='addstock'),
    path('view/<str:choice>/', views.view, name = 'view'),
    path('addSale/', views.addsale, name = 'addSale'),
    path('getProformaInvoice/', views.getProformaInvoice, name= 'getProformaInvoice'), #added 19-08-23
    # path('logout/', views.logout, name='logout'),
    # path('login/', views.login, name='login'),
    path('search/', views.item_search, name="itemSearch"),
    path('editData/', views.editData, name='editData'),
    #XXXXXXXXXXXXXXXXXXX UPDATED:ADDED PARAMETERS TO GET CSV BASED ON CHOICE.
    path('getstock/<str:choice>/<str:value>/', views.getfile, name='getStock'),
     #XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        #Added 23-05-23
    path('restoreData/', views.restoreData, name='restoreData'),
    path('getInfo/', views.getInfo, name='getInfo'),#added 02-06-2023
    path('getOldPdf', views.getOldPdf, name='getOldPdf'),
    path('getQty', views.getQty, name='getQty'),
    path('searchFilter', views.searchFilter, name='searchFilter'),
    path('getDb/', views.getDb, name='getDb'),

    #path('getInfo/<str:item>/<str:width>/<str:rollNo>/', views.getInfo, name='getInfo')#added 01-06-2023

    path('SaleFrmPID', views.addSaleFromProformaID, name="addSaleFromProformaID"),
    # path('getOldPI',views.getOldPI, name="getOldPI")
]

# handler404 = 'app1.views.error_404'
# handler500 = 'app1.views.error_500'