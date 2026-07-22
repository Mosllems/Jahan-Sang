import config.converters
from django.urls import path

from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.BlogView.as_view(), name="blog"),
    path('<uslug:slug>/', views.BlogDetailView.as_view(), name="blog_detail")

]
