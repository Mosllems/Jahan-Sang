import config.converters
from django.urls import path

from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.InventoryListView.as_view(), name='inventory_list'),
    path('stones/create/', views.StoneCreateView.as_view(), name='stone_create'),
    path('tools/create/', views.ToolCreateView.as_view(), name='tool_create'),
    path('stones/<uslug:slug>/', views.StoneDetailView.as_view(), name='stone_detail'),
    path('tools/<uslug:slug>/', views.ToolDetailView.as_view(), name='tool_detail'),
]
