from django.views.generic import TemplateView, ListView

class Index(ListView):
    template_name = "Core/index.html"

    def get_queryset(self):
        return None
