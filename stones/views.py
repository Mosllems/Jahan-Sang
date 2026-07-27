from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import generic


# ---- Sample data (frontend preview only; no model yet) ----
STONE_TYPES = [
    {"slug": "marble", "name": "مرمر"},
    {"slug": "granite", "name": "گرانیت"},
    {"slug": "quartz", "name": "کوارتز"},
    {"slug": "travertine", "name": "تراورتن"},
]

# status: available | limited | out
SAMPLE_STONES = [
    {"name": "مرمر سفید کریستال", "type": "marble", "type_name": "مرمر", "origin": "لاس‌وگاس", "dimensions": "۳۲۰×۱۶۰ سانتی‌متر", "slabs": 12, "status": "available", "image": "imgs/project/project-5.webp"},
    {"name": "گرانیت مشکی گلکسی", "type": "granite", "type_name": "گرانیت", "origin": "هند", "dimensions": "۳۰۰×۱۵۰ سانتی‌متر", "slabs": 4, "status": "limited", "image": "imgs/project/project-6.webp"},
    {"name": "کوارتز کرم رویال", "type": "quartz", "type_name": "کوارتز", "origin": "ترکیه", "dimensions": "۳۱۰×۱۴۰ سانتی‌متر", "slabs": 0, "status": "out", "image": "imgs/project/project-7.webp"},
    {"name": "تراورتن عباس‌آباد", "type": "travertine", "type_name": "تراورتن", "origin": "اصفهان", "dimensions": "۳۰۰×۱۲۰ سانتی‌متر", "slabs": 26, "status": "available", "image": "imgs/project/project-8.webp"},
    {"name": "مرمر امپرادور قهوه‌ای", "type": "marble", "type_name": "مرمر", "origin": "اسپانیا", "dimensions": "۲۹۰×۱۵۰ سانتی‌متر", "slabs": 3, "status": "limited", "image": "imgs/project/project-11.webp"},
    {"name": "گرانیت سفید دلابادی", "type": "granite", "type_name": "گرانیت", "origin": "مشهد", "dimensions": "۳۲۰×۱۶۰ سانتی‌متر", "slabs": 18, "status": "available", "image": "imgs/project/project-5.webp"},
]

STATUS_LABELS = {
    "available": {"label": "موجود", "class": "available"},
    "limited": {"label": "محدود", "class": "limited"},
    "out": {"label": "ناموجود", "class": "out"},
}


class StoneListView(UserPassesTestMixin, generic.TemplateView):
    template_name = "stones/stone_list.html"

    def test_func(self):
        # Only staff/admin users may view this page.
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        stones = []
        for s in SAMPLE_STONES:
            item = dict(s)
            item["status_info"] = STATUS_LABELS[s["status"]]
            stones.append(item)

        query = (self.request.GET.get("q") or "").strip()
        type_filter = self.request.GET.get("type") or ""
        status_filter = self.request.GET.get("status") or ""

        if query:
            stones = [s for s in stones if query in s["name"]]
        if type_filter:
            stones = [s for s in stones if s["type"] == type_filter]
        if status_filter:
            stones = [s for s in stones if s["status"] == status_filter]

        context["stones"] = stones
        context["stone_types"] = STONE_TYPES
        context["statuses"] = [
            {"slug": "available", "name": "موجود"},
            {"slug": "limited", "name": "محدود"},
            {"slug": "out", "name": "ناموجود"},
        ]
        context["q"] = query
        context["active_type"] = type_filter
        context["active_status"] = status_filter
        return context
