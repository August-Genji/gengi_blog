import django_filters
from .models import PostWorkFlow


class PostWorkFlowFilter(django_filters.FilterSet):
    post_title = django_filters.CharFilter(field_name='post__title', lookup_expr='icontains')

    class Meta:
        model = PostWorkFlow
        fields = ['step']  # важно: тут только реальные поля модели
