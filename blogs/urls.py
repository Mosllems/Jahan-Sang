from django.urls import path

from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.BlogView.as_view(), name="blog"),
    path('<int:pk>/', views.BlogDetailView.as_view(), name="blog_detail")
    
]
