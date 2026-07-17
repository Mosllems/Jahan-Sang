from django.shortcuts import render
from django.views import generic

from blogs.models import Blog


class BlogView(generic.TemplateView):
    template_name = "blogs/blog.html"


class BlogDetailView(generic.DetailView):
    template_name = "blogs/blog_detail.html"
    model = Blog
