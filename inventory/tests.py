"""
Tests for the inventory app.

This file is a TEMPLATE — it demonstrates the four kinds of tests you'll
write across the whole project:

    1. MODEL tests      -> pure business logic (no HTTP)
    2. PERMISSION tests -> who is allowed to see what
    3. VIEW tests       -> status codes, context, search/filter
    4. FORM/FLOW tests  -> submitting data actually creates a record

Run everything:      docker compose exec backend python manage.py test
Run only this app:   docker compose exec backend python manage.py test inventory
Run one class:       docker compose exec backend python manage.py test inventory.StoneModelTest
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Stone, StoneCategory, Tool, ToolCategory

User = get_user_model()


# ---------------------------------------------------------------------------
# 1. MODEL TESTS — pure logic, no requests involved.
#    These are the easiest tests to write and the fastest to run.
# ---------------------------------------------------------------------------
class StoneModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Runs ONCE for the whole class. Use it for data that tests only read.
        (Use setUp() instead if a test needs to modify the object.)"""
        cls.category = StoneCategory.objects.create(name="مرمر")

    def test_stock_status_is_out_when_quantity_zero(self):
        stone = Stone.objects.create(name="سنگ صفر", category=self.category, quantity=0)
        self.assertEqual(stone.stock_status, "out")
        self.assertEqual(stone.stock_status_display, "ناموجود")

    def test_stock_status_is_limited_at_or_below_threshold(self):
        # LOW_STOCK_THRESHOLD is 5, so 5 is still "limited" (boundary case!)
        stone = Stone.objects.create(name="سنگ کم", category=self.category, quantity=5)
        self.assertEqual(stone.stock_status, "limited")
        self.assertEqual(stone.stock_status_display, "محدود")

    def test_stock_status_is_available_above_threshold(self):
        stone = Stone.objects.create(name="سنگ زیاد", category=self.category, quantity=6)
        self.assertEqual(stone.stock_status, "available")
        self.assertEqual(stone.stock_status_display, "موجود")

    def test_slug_is_auto_generated_from_persian_name(self):
        """Your save() calls slugify(..., allow_unicode=True) — this proves it works."""
        stone = Stone.objects.create(name="مرمر سفید", category=self.category, quantity=1)
        self.assertEqual(stone.slug, "مرمر-سفید")

    def test_slug_is_not_overwritten_if_provided(self):
        stone = Stone.objects.create(
            name="سنگ دلخواه", category=self.category, quantity=1, slug="custom-slug"
        )
        self.assertEqual(stone.slug, "custom-slug")

    def test_str_returns_name(self):
        stone = Stone.objects.create(name="سنگ نام", category=self.category, quantity=1)
        self.assertEqual(str(stone), "سنگ نام")


class ToolModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = ToolCategory.objects.create(name="برش")

    def test_tool_inherits_stock_status_logic(self):
        """Tool and Stone share the InventoryItem base, so the logic must match."""
        tool = Tool.objects.create(name="اره تست", category=self.category, quantity=0)
        self.assertEqual(tool.stock_status_display, "ناموجود")

    def test_condition_default_is_good(self):
        tool = Tool.objects.create(name="ابزار سالم", category=self.category, quantity=2)
        self.assertEqual(tool.condition, "good")
        self.assertEqual(tool.get_condition_display(), "سالم")


# ---------------------------------------------------------------------------
# 2. PERMISSION TESTS — the highest-value tests in this project.
#    Inventory is internal data: anonymous and normal users must be locked out.
# ---------------------------------------------------------------------------
class InventoryPermissionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # NOTE: mobile_number is unique=True, so every user needs a different one.
        cls.staff = User.objects.create_user(
            username="staff_t", email="staff_t@example.com",
            mobile_number="09120000001", password="StrongPass!234",
        )
        cls.staff.is_staff = True
        cls.staff.save()

        cls.normal = User.objects.create_user(
            username="normal_t", email="normal_t@example.com",
            mobile_number="09120000002", password="StrongPass!234",
        )

        category = StoneCategory.objects.create(name="گرانیت")
        cls.stone = Stone.objects.create(name="سنگ محرمانه", category=category, quantity=3)

        tool_category = ToolCategory.objects.create(name="دستی")
        cls.tool = Tool.objects.create(name="ابزار محرمانه", category=tool_category, quantity=3)

    def _all_inventory_urls(self):
        """Every URL in this app that must be staff-only."""
        return [
            reverse("inventory:inventory_list"),
            reverse("inventory:stone_create"),
            reverse("inventory:tool_create"),
            reverse("inventory:stone_detail", kwargs={"slug": self.stone.slug}),
            reverse("inventory:tool_detail", kwargs={"slug": self.tool.slug}),
        ]

    def test_anonymous_is_redirected_to_login(self):
        for url in self._all_inventory_urls():
            with self.subTest(url=url):          # subTest = report each URL separately
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertIn("/accounts/login/", response.url)

    def test_normal_user_is_forbidden(self):
        self.client.force_login(self.normal)     # force_login skips the password step
        for url in self._all_inventory_urls():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 403)

    def test_staff_user_has_access(self):
        self.client.force_login(self.staff)
        for url in self._all_inventory_urls():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)


# ---------------------------------------------------------------------------
# 3. VIEW TESTS — correct template, correct context, search & filter behaviour.
# ---------------------------------------------------------------------------
class InventoryListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_user(
            username="staff_v", email="staff_v@example.com",
            mobile_number="09120000003", password="StrongPass!234",
        )
        cls.staff.is_staff = True
        cls.staff.save()

        cls.marble = StoneCategory.objects.create(name="مرمر")
        cls.granite = StoneCategory.objects.create(name="گرانیت")

        Stone.objects.create(name="مرمر سفید", category=cls.marble, quantity=10)   # available
        Stone.objects.create(name="مرمر مشکی", category=cls.marble, quantity=0)    # out
        Stone.objects.create(name="گرانیت قرمز", category=cls.granite, quantity=2) # limited

        cls.tool_category = ToolCategory.objects.create(name="برش")
        Tool.objects.create(name="اره برقی", category=cls.tool_category, quantity=4)

    def setUp(self):
        """Runs before EVERY test method — log in each time."""
        self.client.force_login(self.staff)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("inventory:inventory_list"))
        self.assertTemplateUsed(response, "inventory/inventory_list.html")

    def test_defaults_to_stones_tab(self):
        response = self.client.get(reverse("inventory:inventory_list"))
        self.assertEqual(response.context["active_tab"], "stones")
        self.assertEqual(len(response.context["items"]), 3)

    def test_tools_tab_shows_tools(self):
        response = self.client.get(reverse("inventory:inventory_list"), {"tab": "tools"})
        self.assertEqual(response.context["active_tab"], "tools")
        self.assertEqual(len(response.context["items"]), 1)

    def test_invalid_tab_falls_back_to_stones(self):
        response = self.client.get(reverse("inventory:inventory_list"), {"tab": "banana"})
        self.assertEqual(response.context["active_tab"], "stones")

    def test_search_filters_by_name(self):
        response = self.client.get(reverse("inventory:inventory_list"), {"q": "گرانیت"})
        items = response.context["items"]
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].name, "گرانیت قرمز")

    def test_category_filter(self):
        response = self.client.get(
            reverse("inventory:inventory_list"), {"category": self.marble.slug}
        )
        self.assertEqual(len(response.context["items"]), 2)

    def test_status_filter(self):
        response = self.client.get(reverse("inventory:inventory_list"), {"status": "out"})
        items = response.context["items"]
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].name, "مرمر مشکی")

    def test_response_contains_stone_name(self):
        """assertContains checks the rendered HTML, not just the context."""
        response = self.client.get(reverse("inventory:inventory_list"))
        self.assertContains(response, "مرمر سفید")


# ---------------------------------------------------------------------------
# 4. FORM / FLOW TESTS — does POSTing valid data actually create a record?
#    (This is the class of bug that hit the contact form: it looked fine but
#     never saved, because the <form> had no method="post".)
# ---------------------------------------------------------------------------
class StoneCreateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_user(
            username="staff_c", email="staff_c@example.com",
            mobile_number="09120000004", password="StrongPass!234",
        )
        cls.staff.is_staff = True
        cls.staff.save()
        cls.category = StoneCategory.objects.create(name="کوارتز")

    def setUp(self):
        self.client.force_login(self.staff)

    def test_valid_post_creates_stone_and_redirects(self):
        response = self.client.post(reverse("inventory:stone_create"), {
            "name": "سنگ جدید",
            "category": self.category.id,
            "quantity": 7,
            "origin": "اصفهان",
            "dimensions": "300x150",
            "thickness": "2cm",
        })
        self.assertRedirects(response, reverse("inventory:inventory_list"))

        stone = Stone.objects.get(name="سنگ جدید")
        self.assertEqual(stone.quantity, 7)
        self.assertEqual(stone.stock_status, "available")
        self.assertEqual(stone.slug, "سنگ-جدید")      # auto-slug worked

    def test_invalid_post_does_not_create_stone(self):
        """Missing required 'name' -> form redisplays with an error, nothing saved."""
        response = self.client.post(reverse("inventory:stone_create"), {
            "name": "",
            "category": self.category.id,
            "quantity": 7,
        })
        self.assertEqual(response.status_code, 200)          # re-rendered, not redirected
        self.assertFormError(response.context["form"], "name", "This field is required.")
        self.assertEqual(Stone.objects.count(), 0)
