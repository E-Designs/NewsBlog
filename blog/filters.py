import django_filters
from .models import Post

class postFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ['title', 'subject', 'city', 'state', 'country']