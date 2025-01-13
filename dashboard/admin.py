from django.contrib import admin
from .models import BlogModel

# Register your models here.

@admin.register(BlogModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'draft', 'image', 'file_directory')
    prepopulated_fields = {'slug': ('title',)}


