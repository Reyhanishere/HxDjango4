from django.views.generic import ListView
from .models import Post

class PostsList(ListView):
    model = Post
    template_name = "pages/posts_list.html"
