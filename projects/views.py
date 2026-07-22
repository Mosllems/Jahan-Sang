from django.views import generic
from django.db.models import Prefetch

from projects.models import Project, ProjectCategory, ProjectImage


class ProjectListView(generic.ListView):
    paginate_by = 6
    model = Project
    template_name = 'projects/project.html'
    context_object_name = 'projects'

    def get_queryset(self):
        cover_prefetch = Prefetch('images', queryset=ProjectImage.objects.order_by('-is_cover', 'datetime_created'), to_attr='prefetched_covers')

        queryset = Project.objects.select_related('category').prefetch_related(cover_prefetch)
        sorted_projects = self.request.GET.get('sort')
        if sorted_projects:
            queryset = queryset.filter(category__slug=sorted_projects)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProjectCategory.objects.all()
        return context


class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = "projects/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        cover_prefetch = Prefetch('images', queryset=ProjectImage.objects.order_by('-is_cover', 'datetime_created'), to_attr='prefetched_covers')
        queryset = Project.objects.select_related('category').prefetch_related(cover_prefetch)

        return queryset

