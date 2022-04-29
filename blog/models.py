from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def get_comments(self):
        return self.comments.filter(parent=None)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # some comments may not have parent Comment, so put null=True for db and blank=True for form check
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=100)

    class Meta:
        ordering = ('date_posted',)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def get_comments(self):
        return Comment.objects.filter(parent=self)

