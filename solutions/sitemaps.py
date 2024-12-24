from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Solution

class StaticViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return [
            'solutions:solution-list',
            'solutions:tag-list',  
        ]

    def location(self, item):
        return reverse(item)

class SolutionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Solution.objects.all()

    def lastmod(self, obj):
        return obj.modified_date
