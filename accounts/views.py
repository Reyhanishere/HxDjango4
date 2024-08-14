from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm
import cases.models as Cases

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"

def user_panel(request):
    user = request.user
    hxs = Cases.Case.objects.filter(author=user)
    return render(request, 'user/user_panel.html', {'hxs': hxs,})
