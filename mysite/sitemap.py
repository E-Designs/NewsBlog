from django.contrib import sitemaps 
from blog.models import Post
from django.urls import reverse
from django.db.models import Q
from blog.utility import Visability_State
class StaticSitemap(sitemaps.Sitemap):

    changefreq= 'weakly'
    priority = 0.5

    def items(self):
        return ['post_about', 'post_list', 'games','tou' ]

    def location(self, item):
        return reverse(item)

class dynamicSitemap(sitemaps.Sitemap):

    changefreq = 'weakly'
    priority = 0.5

    def items(self):
        return Post.objects.filter(Q(visability= Visability_State.pending) | Q(visability= Visability_State.approved))
