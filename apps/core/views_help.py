from django.views.generic import TemplateView


class MarkdownHelpView(TemplateView):
    """صفحه راهنمای Markdown"""
    template_name = "core/help/markdown.html"
