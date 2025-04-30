from django.contrib import admin
from .models import Like,  Post, Comment, Favorite, Profile

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Favorite)
admin.site.register(Profile)
