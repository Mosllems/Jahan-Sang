from django.views import generic

from projects.models import Project, ProjectCategory


class ProjectListView(generic.ListView):
    paginate_by = 6
    model = Project
    template_name = 'projects/project.html'
    context_object_name = 'projects'

    def get_queryset(self):
        queryset = Project.objects.select_related('category').prefetch_related('images').all()
        sorted_projects = self.request.GET.get('sort')
        if sorted_projects:
            queryset = queryset.filter(category__slug=sorted_projects)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProjectCategory.objects.all()
        return context
