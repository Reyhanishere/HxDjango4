from django.views.generic import ListView, DetailView

from .models import Doc


# Create your views here.
class DocsListView(ListView):
    model = Doc
    template_name = "pages/docs_list.html"


class DocDetailView(DetailView):
    model=Doc
    template_name="pages/doc_detail.html"
