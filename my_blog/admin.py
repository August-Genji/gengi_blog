from django.contrib import admin
from .models import Like, Post, Comment, Favorite, Profile, PostWorkFlow

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Favorite)
admin.site.register(Profile)


@admin.register(PostWorkFlow)
class PostWorkFlowAdmin(admin.ModelAdmin):
    list_display = ('post', 'step', 'timestamp')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
