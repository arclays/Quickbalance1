#endpoints
from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.client_list_create, name='client-list'),
    path('create/', views.client_list_create, name='client-create'),
    path('<int:pk>/', views.client_detail, name='client-detail'),
    path('<int:pk>/update/', views.client_detail, name='client-update'),
    path('<int:pk>/partial-update/', views.client_detail, name='client-partial-update'),
    path('<int:pk>/delete/', views.client_detail, name='client-delete'),
    path('search/', views.client_search, name='client-search'),
    path('stats/', views.client_stats, name='client-stats'),
]