from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Group, Post
from .forms import PostForm

POST_SHOW = 10

User = get_user_model()

def pagination(request, group):
    paginator = Paginator(group, POST_SHOW)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

def index(request):
    template = 'posts/index.html'
    title = 'Это главная страница проекта Mypipe'
    posts = Post.objects.select_related('author', 'group')
    page_obj = pagination(request, posts)
    context = {
        'title': title,
        'posts': posts,
        'page_obj': page_obj
    }
    return render(request, template, context)

def profile(request, username):
    template = 'posts/profile.html'
    title = 'Страница пользователя'
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related('author', 'group')
    page_obj = pagination(request, posts)
    context = {
        'title': title,
        'posts': posts,
        'author': author,
        'page_obj': page_obj
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

def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    title = 'подробная информация'
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'title': title,
        'post': post,
    }
    return render(request, template, context)

@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author_id = request.user.id
        new_post.save()
        return redirect('posts:index')
    return render(request, 'posts/create_post.html', context)