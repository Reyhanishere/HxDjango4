from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = "pages/index.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


class TermsPageView(TemplateView):
    template_name = "pages/terms.html"

class GraphsPageView(TemplateView):
    template_name = "pages/graph.html"
