from django.shortcuts import render
from django.views.generic import ListView
from .models import Post

class PostsList(ListView):
    model = Post
    template_name = "posts_list.html"