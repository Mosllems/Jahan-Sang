from django.shortcuts import render
from django.views import generic


class ProjectListView(generic.TemplateView):
    template_name = 'projects/project.html'

