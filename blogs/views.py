from django.shortcuts import render
from django.views import generic

from blogs.models import Blog, Category


class BlogView(generic.ListView):
    model = Blog
    template_name = "blogs/blog.html"

    def get_queryset(self):
        return Blog.objects.select_related('category', 'author').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['blogs'] = self.get_queryset()
        return context


class BlogDetailView(generic.DetailView):
    model = Blog
    template_name = "blogs/blog_detail.html"
    context_object_name = "blog"

