from django.urls import path, register_converter

from . import views
from .converters import UnicodeSlugConverter

register_converter(UnicodeSlugConverter, "uslug")

app_name = 'blogs'

urlpatterns = [
    path('', views.BlogView.as_view(), name="blog"),
    path('<uslug:slug>/', views.BlogDetailView.as_view(), name="blog_detail")

]
