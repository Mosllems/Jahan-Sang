from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.views import generic

from blogs.forms import CommentForm
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

    def get_queryset(self):
        return Blog.objects.select_related('author', 'category').prefetch_related('comments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['recent_blogs'] = Blog.objects.select_related('category', 'author')[:3]
        context['comments'] = self.object.comments.filter(is_approved=True).select_related('author').prefetch_related('blog')
        context['comment_form'] = kwargs.get('comment_form') or CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.blog = self.object
            comment.save()
            messages.success(request, "نظر شما ثبت شد و پس از تأیید نمایش داده می‌شود.")
            return redirect(self.object.get_absolute_url())

        context = self.get_context_data(comment_form=form)
        return self.render_to_response(context)
