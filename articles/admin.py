# articles/admin.py
from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_published')
    list_filter = ('is_published', 'published_date', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'author')
        }),
        ('Publication Info', {
            'fields': ('is_published', 'published_date', 'updated_date'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('published_date', 'updated_date')