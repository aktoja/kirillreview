from django.shortcuts import render
from .models import Post, Group
from django.shortcuts import get_object_or_404


def index(request):
    template = 'posts/index.html'
    title = 'Это главная страница проекта Mypipe'
    posts = Post.objects.select_related('author')[:10]
    context = {
        'title': title,
        'posts': posts
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    title = 'Здесь будет информация о группах проекта Mypipe'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author')[:10]
    context = {
        'title': title,
        'group': group,
        'posts': posts
    }
    return render(request, template, context)
