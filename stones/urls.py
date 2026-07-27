from django.urls import path

from . import views

app_name = 'stones'

urlpatterns = [
    path('', views.StoneListView.as_view(), name='stone_list'),
]
