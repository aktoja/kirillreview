from django.shortcuts import get_object_or_404, render

from .models import Group, Post

POST_SHOW = 10


def index(request):
    template = 'posts/index.html'
    title = 'Это главная страница проекта Mypipe'
    posts = Post.objects.select_related('author')[:POST_SHOW]
    context = {
        'title': title,
        'posts': posts
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    title = 'Здесь будет информация о группах проекта Mypipe'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author')[:POST_SHOW]
    context = {
        'title': title,
        'group': group,
        'posts': posts
    }
    return render(request, template, context)
