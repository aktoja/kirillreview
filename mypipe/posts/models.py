from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название группы')
    slug = models.SlugField(unique=True, verbose_name="Читаемый url")
    description = models.TextField(verbose_name="Описание группы")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class Post(models.Model):
    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name="Дата публикации")
    image = models.ImageField(blank=True, upload_to='posts/',
                              verbose_name="Картинка")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Автор")
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name="Группа"
    )

    def __str__(self):
        return self.text[:25]

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    text = models.CharField(max_length=300,
                            verbose_name="Текст")
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name="Дата публикации")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Автор"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Пост"
    )

    def __str__(self):
        return self.text[:25]

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name="Подписчик"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name="Автор"
    )

    class Meta:
        constraints = (models.UniqueConstraint(fields=['user', 'author'],
                                               name='unique_subscribe'),)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
