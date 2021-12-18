from django.contrib import admin
from .models import Post
from django import forms

"""

Цель: регистрация классов в админ-панели
"""


class PostAdmin(admin.ModelAdmin):
    model = Post


admin.site.register(Post, PostAdmin)
