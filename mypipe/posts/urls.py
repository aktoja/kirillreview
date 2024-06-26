from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
    path('create/', views.post_create, name='post_create'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('post_detail/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post_detail/<int:post_id>/comment',
         views.add_comment, name='add_comment'),
    path('post_detail/<int:post_id>/edit', views.post_edit, name='post_edit'),
    path('subscribe/', views.subscribe_index,
         name='subscribe_index'),
    path('profile/<str:username>/subscribe',
         views.subscribe, name='subscribe'),
    path('profile/<str:username>/unsubscribe',
         views.unsubscribe, name='unsubscribe'),
]
