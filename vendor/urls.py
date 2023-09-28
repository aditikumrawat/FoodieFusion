from django.urls import path
from . import views

urlpatterns = [
    path('registerVendor/', views.registerVendor, name = 'registerVendor'),
    path('vendorDashboard/', views.vendorDashboard, name = 'vendorDashboard'),
]
