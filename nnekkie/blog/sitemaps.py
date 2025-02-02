from django.contrib.sitemaps import Sitemap
from .models import *
from django.urls import reverse



class BlogSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1
    def items(self):
        return Blog.objects.filter(active=True)
    
    def lastmod(self, obj):
        return obj.date
    def location(self, obj):
        return reverse('blog:index')
    def title(self, obj):
        return obj.title
    def file_url(self, obj):
        if obj.file:
            return [obj.file.url]
        return []
    def get_urls(self, site=None, **kwargs):
        urls = super().get_urls(site=site, **kwargs)
        for url in urls:
            item = url['item']
            file_list = self.file_urls(item)
            if file_list:
                url['files'] = [{'loc':file_url} for file_url in file_list]
        return urls

    