from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name','lang_code','slug', 'mime', 'created_on']
    search_fields = ['name', 'file_extension']
    ordering = ['name']
    list_filter = ['created_on']
    date_hierarchy = 'created_on'
    # fields = ['name','slug','lang_code','mime','created_on']

class SnippetAdmin(admin.ModelAdmin):
    list_display = ['language', 'title', 'expiration', 'exposure', 'user']
    search_fields = ['title','user']
    ordering = ['-created_on']
    list_filter = ['created_on']
    date_hierarchy = 'created_on'
    # filter_horizontal = ('tags',)
    raw_id_fields = ('tags',)
    readonly_fields = ('highlighted_code','hits','slug',)
    fields = ('title', 'original_code', 'highlighted_code', 'expiration', 'exposure',
              'hits', 'slug', 'language', 'user', 'tags')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class AuthorInline(admin.TabularInline):
    model=models.Author

class CustomerUserAdmin(UserAdmin):
    inlines=(AuthorInline, )

admin.site.unregister(User)
admin.site.register(User, CustomerUserAdmin)
admin.site.register(models.Language, LanguageAdmin)
admin.site.register(models.Snippet, SnippetAdmin)
admin.site.register(models.Tag, TagAdmin)
