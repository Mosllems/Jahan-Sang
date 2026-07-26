import json
from django.forms.models import BaseModelForm
import requests
import logging
import uuid

from datetime import datetime, timezone
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.contrib import messages

from .models import ContactForm
from .forms import Contact

logger = logging.getLogger(__name__)

FALLBACK_REPLY = "با عرض پوزش، ربات گفتگو هنوز فعال نشده است. لطفاً بعداً دوباره تلاش کنید یا از طریق فرم تماس با ما در ارتباط باشید."
HISTORY_SESSION_KEY = "chat_history"
SESSION_ID_KEY = "chat_session_id"
MAX_HISTORY_MESSAGES = 40
MAX_MESSAGE_LENGTH = 2000

class HomeView(generic.TemplateView):
    template_name = "pages/home.html"


class AboutView(generic.TemplateView):
    template_name = "pages/about.html"


class ContactView(generic.CreateView):
    model = ContactForm
    form_class = Contact
    template_name='pages/contact.html'
    success_url = reverse_lazy('pages:contact')

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs() # first get the kwargs of the django
        kwargs['user'] = self.request.user # add our user to the kwargs of the django 

        return kwargs

    def form_valid(self, form: BaseModelForm):

        if self.request.user.is_authenticated:
            form.instance.author = self.request.user
            form.instance.first_name = self.request.user.first_name
            form.instance.last_name = self.request.user.last_name
            form.instance.phone_number = self.request.user.mobile_number
            form.instance.email = self.request.user.email

        messages.success(self.request, "پیام شما با موفقیت ارسال شد.")

        return super().form_valid(form)



@require_POST
def chat_message(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "invalid json"}, status=400)

    text = (data.get("message") or "").strip()
    if not text or len(text) > MAX_MESSAGE_LENGTH:
        return JsonResponse({"error": "invalid message"}, status=400)

    chat_session_id = request.session.setdefault(SESSION_ID_KEY, str(uuid.uuid4()))

    reply_text = FALLBACK_REPLY
    if settings.N8N_WEBHOOK_URL:
        try:
            resp = requests.post(
                settings.N8N_WEBHOOK_URL,
                json={"message": text, "sessionId": chat_session_id},
                timeout=settings.N8N_WEBHOOK_TIMEOUT,
            )
            resp.raise_for_status()
            reply_text = resp.json().get("reply") or FALLBACK_REPLY
        except (requests.exceptions.RequestException, ValueError) as exc:
            logger.warning("n8n webhook call failed: %s", exc)
            reply_text = FALLBACK_REPLY

    now = datetime.now(timezone.utc).isoformat()
    history = request.session.get(HISTORY_SESSION_KEY, [])
    history.append({"role": "user", "text": text, "ts": now})
    history.append({"role": "bot", "text": reply_text, "ts": now})
    request.session[HISTORY_SESSION_KEY] = history[-MAX_HISTORY_MESSAGES:]
    request.session.modified = True

    return JsonResponse({"reply": reply_text})
