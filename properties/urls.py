from django.urls import path
from properties import views as v

urlpatterns = [
    path('', v.property_list, name='property-list')
]