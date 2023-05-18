from django.urls import path
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('main/', views.main, name = "main"),
    path('client_enter/', views.client_enter, name = "client_enter"),
    path('worker_enter/', views.worker_enter, name = "worker_enter"),
    path('search_worker/', views.search_worker, name = "search_worker"),
    path('search_client/', views.search_client, name = "search_client"),
    path('error/', views.error, name = "error"),
    path('search_error/', views.search_error, name = "search_error"),
    path('logout/', views.LogoutView.as_view(), name = "logout"),
    
]