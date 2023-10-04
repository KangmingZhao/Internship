from django.contrib import admin
from django.urls import path,include
from .views import index,main_view,entry_view

urlpatterns = [
	path('', entry_view), 
	path('main_view',main_view),
]


