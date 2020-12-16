import django_filters
from .models import *

class PostFilter(django_filters.FilterSet):
    post_type = django_filters.CharFilter(field_name='post_type', method='filter_post_type')

    def filter_post_type(self, qs, name, value):
        return qs.filter(**{name:value})

    class Meta:
        model = Post
        fields = ['post_type']