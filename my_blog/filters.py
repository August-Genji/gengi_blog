import django_filters

from .models import PostWorkFlow, Post


class PostWorkFlowFilter(django_filters.FilterSet):
    post_title = django_filters.CharFilter(field_name='post__title', lookup_expr='icontains')

    class Meta:
        model = PostWorkFlow
        fields = ['step']  # важно: тут только реальные поля модели


class PostFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(field_name='author__username', lookup_expr='icontains')
    created_date = django_filters.DateFilter(field_name='created_date', lookup_expr='exact')
    created_date__gte = django_filters.DateFilter(field_name='created_date', lookup_expr='gte')
    created_date__lte = django_filters.DateFilter(field_name='created_date', lookup_expr='lte')

    class Meta:
        model = Post
        fields = ['title', 'created_date', 'update_date']