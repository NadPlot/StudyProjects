from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Category, Respond


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Respond)