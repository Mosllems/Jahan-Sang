"""Load sample content so a fresh clone of the project has something to show.

    python manage.py load_demo

Safe to run more than once (existing demo rows are left alone). Images are
copied from the template's own static/imgs/gallery/ folder, so no extra files
need to be stored in the repository.
"""

from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from blogs.models import Blog, Category
from inventory.models import Stone, StoneCategory, Tool, ToolCategory
from projects.models import Project, ProjectCategory, ProjectImage

GALLERY = Path(settings.BASE_DIR) / "static" / "imgs" / "gallery"

BLOG_TEXT = """## معرفی سنگ‌های ساختمانی

انتخاب سنگ مناسب برای نما و کف، یکی از **مهم‌ترین تصمیم‌های** هر پروژه‌ی ساختمانی است.

### نکته‌های انتخاب سنگ

- مقاومت در برابر سایش و رطوبت
- هماهنگی رنگ و طرح با طراحی ساختمان
- قیمت و هزینه‌ی نصب

> برای نمای بیرونی از سنگ‌هایی با **جذب آب پایین** استفاده کنید.

| نوع سنگ | کاربرد |
|---|---|
| مرمریت | نما و کف |
| گرانیت | پله و آشپزخانه |
| تراورتن | نمای ساختمان |

برای مشاوره‌ی بیشتر با ما تماس بگیرید.
"""

PROJECT_TEXT = """این پروژه شامل **تأمین و نصب سنگ** نمای ساختمان است.

- اجرای نما با سنگ طبیعی
- نصب کف و پله
- بازدید و کنترل کیفیت در همه‌ی مراحل
"""


class Command(BaseCommand):
    help = "Create sample categories, projects, articles and inventory."

    def _image(self, number):
        path = GALLERY / f"gallery-{number}.webp"
        if not path.exists():
            return None
        return path

    def _attach(self, field, number, name):
        path = self._image(number)
        if path:
            with path.open("rb") as fh:
                field.save(name, File(fh), save=False)

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        author, created = User.objects.get_or_create(
            username="demo",
            defaults={"email": "demo@example.com", "mobile_number": "09000000000",
                      "first_name": "نویسنده", "last_name": "نمونه"},
        )
        if created:
            author.set_unusable_password()
            author.save()

        # Articles
        categories = [Category.objects.get_or_create(name=n)[0] for n in ("سنگ‌های ساختمانی", "راهنمای خرید")]
        for i, title in enumerate(("راهنمای انتخاب سنگ نما", "تفاوت مرمریت و گرانیت", "نگهداری از سنگ کف"), start=1):
            if Blog.objects.filter(title=title).exists():
                continue
            blog = Blog(author=author, category=categories[i % 2], title=title, text=BLOG_TEXT)
            self._attach(blog.photo, 28 + i, f"demo-blog-{i}.webp")
            blog.save()

        # Projects
        project_cats = [ProjectCategory.objects.get_or_create(name=n)[0] for n in ("نمای ساختمان", "کف و پله")]
        for i, (title, place) in enumerate((("پروژه‌ی نمای ویلا", "اصفهان"), ("پروژه‌ی کف مجتمع تجاری", "نطنز"),
                                            ("پروژه‌ی پله‌های برج", "تهران")), start=1):
            if Project.objects.filter(title=title).exists():
                continue
            project = Project.objects.create(category=project_cats[i % 2], title=title, description=PROJECT_TEXT,
                                             client="مشتری نمونه", location=place)
            for j in range(2):
                img = ProjectImage(project=project, is_cover=(j == 0))
                self._attach(img.image, 20 + i + j, f"demo-project-{i}-{j}.webp")
                img.save()

        # Inventory
        stone_cat, _ = StoneCategory.objects.get_or_create(name="سنگ نما")
        for name, qty in (("گرانیت نطنز", 40), ("مرمریت سفید", 3), ("تراورتن", 0)):
            if not Stone.objects.filter(name=name).exists():
                stone = Stone(category=stone_cat, name=name, quantity=qty, origin="ایران", dimensions="60x60", thickness="2cm")
                self._attach(stone.image, 15, f"demo-stone-{qty}.webp")
                stone.save()
        tool_cat, _ = ToolCategory.objects.get_or_create(name="ابزار برش")
        if not Tool.objects.filter(name="دستگاه سنگ‌بر").exists():
            Tool.objects.create(category=tool_cat, name="دستگاه سنگ‌بر", quantity=4, brand="نمونه")

        self.stdout.write(self.style.SUCCESS(
            f"Demo data ready: {Blog.objects.count()} articles, {Project.objects.count()} projects, "
            f"{Stone.objects.count()} stones, {Tool.objects.count()} tools."))
        self.stdout.write("Create an admin login with: python manage.py createsuperuser")
