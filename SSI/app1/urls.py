from django.urls import path
from . import views
from django.views.generic import RedirectView


app_name = 'app1'

urlpatterns = [
    path("addcustomer/", views.addcustomer, name='addcustomer'),
    path('addstock/', views.addStock, name='addstock'),
    path('view/<str:choice>/', views.view, name = 'view'),
    # path('view/stock/', views.view, name = 'view'),
    path('addsale/', views.addsale, name = 'sell'),
    path('', RedirectView.as_view(url='view/stock')),
    # path('temp/', views.query, name = 'temp')
    # path('logout/', views.logout, name='logout'),
    # path('login/', views.login, name='login'),
    path('search/', views.item_search, name="itemSearch"),
    path('editdata/', views.editData, name='editData'),
    path('getstock/', views.getfile, name='getStock'),
     #XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        #Added 23-05-23
    path('restoredata/', views.restoreData, name='restoreData')

]

# handler404 = 'app1.views.error_404'
# handler500 = 'app1.views.error_500'