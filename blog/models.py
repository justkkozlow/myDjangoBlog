from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    """Создание моделей Post"""

    class Status(models.TextChoices):
        DRAFT = 'DF', "Draft"
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250,
                             verbose_name='Название')
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts',
                               verbose_name='Автор')
    body = models.TextField(verbose_name='Текст статьи')
    publish = models.DateTimeField(default=timezone.now,
                                   verbose_name='Дата публикации')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT,
                              verbose_name='Статус')
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments',
                             verbose_name='Выбрать статью')
    name = models.CharField(max_length=80,
                            verbose_name='Имя')
    email = models.EmailField(verbose_name='E-Mail')
    body = models.TextField(blank=True,
                            null=True,
                            verbose_name='Текст комментария')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Дата обновления')
    active = models.BooleanField(default=True,
                                 verbose_name='Активный')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Комментарий от {self.name} на {self.post}'
