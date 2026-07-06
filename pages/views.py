from django.views import generic


class HomeView(generic.TemplateView):
    template_name = "pages/home.html"


class AboutView(generic.TemplateView):
    template_name = "pages/about.html"

class ContactView(generic.TemplateView):
    template_name = "pages/contact.html"