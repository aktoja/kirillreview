from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Group, Post, Subscription
from .forms import PostForm, CommentForm

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
    form = CommentForm()
    comments = post.comments.all()
    context = {
        'title': title,
        'post': post,
        'form': form,
        'comments': comments,
        }
    return render(request, template, context)

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.author = request.user
        new_comment.post = post
        new_comment.save()
    return redirect('posts:post_detail', post_id=post_id)



@login_required
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    context = {
        'form': form
    }
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author_id = request.user.id
        new_post.save()
        return redirect('posts:index')
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        redirect('post:post_detail', post_id=post_id)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'post': post,
        'form': form,
        'is_edit': True, 
    }
    return render(request, 'posts/create_post.html', context)

@login_required
def subscribe(request, username):
    subscriber = request.user
    author = get_object_or_404(User, username=username)
    if subscriber != author:
        Subscription.objects.get_or_create(subscriber=subscriber,  author=author)
    return redirect('posts:profile', username=username)

@login_required
def unsubscribe(request, username):
    subscriber = request.user
    author = get_object_or_404(User, username=username)
    Subscription.objects.filter(subscriber=subscriber, author=author).delete()
    return redirect('posts:profile', username=username)

@login_required
def subscribe_index(request):
    title = 'Избраное'
    posts = Post.objects.filter(author__subscriber__user=request.user)
    page_obj = pagination(request, posts)
    context = {
        'posts': posts,
        'page_obj': page_obj,
        'title': title
    }
    return render(request, 'posts/subscribe.html', context)





