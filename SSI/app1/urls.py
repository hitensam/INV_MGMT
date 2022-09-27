from django.urls import path
from . import views
from django.views.generic import RedirectView


app_name = 'app1'

urlpatterns = [
    path("customer/", views.addcustomer, name='addcustomer'),
    path('stockadd/', views.addStock, name='addstock'),
    path('view/<str:choice>/', views.view, name = 'view'),
    # path('view/stock/', views.view, name = 'view'),
    path('sell/', views.sell, name = 'sell'),
    path('', RedirectView.as_view(url='view/stock')),
    # path('temp/', views.query, name = 'temp')
    # path('logout/', views.logout, name='logout'),
    # path('login/', views.login, name='login'),
    path('search/', views.item_search, name="itemSearch")
]