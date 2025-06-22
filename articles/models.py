# articles/models.py
from django.db import models
from django.conf import settings
from django.urls import reverse
from ckeditor.fields import RichTextField

class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, help_text="A short label for the URL, contains only letters, numbers, underscores or hyphens.")
    content = RichTextField() # <--- CHANGE THIS LINE
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='articles'
    )
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, help_text="Uncheck to draft the article.")

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})