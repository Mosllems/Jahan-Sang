from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import generic

from .models import Stone, StoneCategory, Tool, ToolCategory

STATUSES = [
    {"slug": "available", "name": "موجود"},
    {"slug": "limited", "name": "محدود"},
    {"slug": "out", "name": "ناموجود"},
]


class InventoryListView(UserPassesTestMixin, generic.TemplateView):
    template_name = "inventory/inventory_list.html"

    def test_func(self):
        # Only staff/admin users may view this page.
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        

        active_tab = self.request.GET.get("tab") or "stones"
        if active_tab not in ("stones", "tools"):
            active_tab = "stones"

        query = (self.request.GET.get("q") or "").strip()
        category_filter = self.request.GET.get("category") or ""
        status_filter = self.request.GET.get("status") or ""

        if active_tab == "tools":
            items = Tool.objects.select_related("category").all()
            categories = ToolCategory.objects.all()
        else:
            items = Stone.objects.select_related("category").all()
            categories = StoneCategory.objects.all()

        if query:
            items = items.filter(name__icontains=query)
        if category_filter:
            items = items.filter(category__slug=category_filter)

        # stock_status is a computed property (not a DB field), so filter in Python.
        items = list(items)
        if status_filter:
            items = [i for i in items if i.stock_status == status_filter]

        context["active_tab"] = active_tab
        context["items"] = items
        context["categories"] = categories
        context["statuses"] = STATUSES
        context["q"] = query
        context["active_category"] = category_filter
        context["active_status"] = status_filter
        return context