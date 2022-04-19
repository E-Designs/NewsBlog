import imp
from django.contrib import sitemaps 
from blog.models import Post
from django.urls import reverse

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
        return Post.objects.all()
