"""Template filters for rendering Markdown article text safely.

Usage in templates:
    {% load markdown_extras %}
    {{ blog.text|markdown }}                      -> formatted HTML
    {{ blog.text|markdown_plain|truncatewords:20 }} -> plain-text preview
"""

import html

import markdown as md
import nh3
from django import template
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

register = template.Library()

MARKDOWN_EXTENSIONS = [
    "extra",       # tables, fenced code blocks, footnotes, abbreviations, ...
    "sane_lists",  # more predictable list behaviour
    "nl2br",       # a single newline becomes <br>, so plain-text posts keep their lines
]

# Keep code-block language classes (e.g. "language-python") so they can be styled.
ALLOWED_ATTRIBUTES = {
    **nh3.ALLOWED_ATTRIBUTES,
    "code": {"class"},
}


def _render(text):
    raw_html = md.markdown(text or "", extensions=MARKDOWN_EXTENSIONS, output_format="html")
    # Strip anything dangerous (<script>, onclick=, javascript: links, ...).
    return nh3.clean(raw_html, attributes=ALLOWED_ATTRIBUTES)


@register.filter(name="markdown")
def markdown_to_html(text):
    """Convert Markdown to sanitized HTML."""
    return mark_safe(_render(text))


@register.filter(name="markdown_plain")
def markdown_to_plain(text):
    """Convert Markdown to plain text (for previews/excerpts)."""
    return html.unescape(strip_tags(_render(text))).strip()
