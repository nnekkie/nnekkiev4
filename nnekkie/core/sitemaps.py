from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post

# class StaticSitemap(Sitemap):
#     def items(self):
#         return ['about']
    
#     def location(self, obj):
#         return reverse(obj)
    
class PostSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return Post.objects.filter(visibility='Everyone')
    def lastmod(self, obj):
        return obj.date
    def location(self, obj):
        return reverse('core:feed')
    def title(self, obj):
        return obj.title
    