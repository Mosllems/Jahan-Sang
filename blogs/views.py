from django.shortcuts import render
from django.views import generic

from blogs.models import Blog, Category


class BlogView(generic.ListView):
    paginate_by = 2
    model = Blog
    template_name = "blogs/blog.html"

    def get_queryset(self):
        queryset = Blog.objects.select_related('category', 'author').all()
        sorted_blogs = self.request.GET.get('sort')
        searched_blogs = self.request.GET.get('q')
        if sorted_blogs:
            queryset = queryset.filter(category__slug=sorted_blogs)
        if searched_blogs:
            queryset = queryset.filter(title__icontains=searched_blogs)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['blogs'] = context['object_list']
        context['recent_blogs'] = self.get_queryset()[:3]
        return context


class BlogDetailView(generic.DetailView):
    model = Blog
    template_name = "blogs/blog_detail.html"
    context_object_name = "blog"

