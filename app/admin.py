from django.contrib import admin

from app.models import Publication


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'time_create', 'is_published']
    list_display_links = ['id', 'title']
    ordering = ['-time_create']
    list_editable = ('is_published',)