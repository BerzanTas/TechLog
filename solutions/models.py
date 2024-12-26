from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
import markdown
import re
from PIL import Image

class Solution(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    content_html = models.TextField(blank=True)
    published_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(null=True, blank=True)
    thumb = models.ImageField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    views_count = models.IntegerField(default=0)
    tags = models.CharField(max_length=200, blank=True)
    
    def save(self, *args, **kwargs):
        # Generate HTML from markdown
        self.content_html = markdown.markdown(self.content)

        if not self.pk:  # If the object is new, generate slug
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1

            while Solution.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug

        if self.pk:  # If object already exist, change modified_date
            self.modified_date = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
    
    def snippet(self):
        plain_text = strip_tags(self.content_html)
        return plain_text[:100] + '...'

    def get_absolute_url(self):
        return reverse('solutions:detail', kwargs={
            'username': self.author.username,
            'slug': self.slug
        })
    
class Comment(models.Model):
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Comment by {self.author} on {self.solution}'