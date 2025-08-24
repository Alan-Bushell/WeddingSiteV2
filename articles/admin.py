# articles/admin.py
from django.contrib import admin
from .models import Article
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class ArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Article
        fields = '__all__'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title', 'author', 'published_date', 'is_published')
    list_filter = ('is_published', 'published_date', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'header_image', 'content', 'author') # ADDED 'header_image' HERE
        }),
        ('Publication Info', {
            'fields': ('is_published', 'published_date', 'updated_date'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('published_date', 'updated_date')