from django.shortcuts import render
from django.views import generic


class BlogView(generic.TemplateView):
    template_name = "blogs/blog.html"

