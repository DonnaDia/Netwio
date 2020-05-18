"""Creates data representation to be saved in the database."""
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Post(models.Model):
    """Creates a Post DB model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    body = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def get_absolute_url(self):
        """Returns absolute url path."""
        return reverse('netwio:post', kwargs={'pk': self.pk})

    def __str__(self):
        return '"{title}" by {username}'.format(title=self.title,
                                                username=self.user.username)

class Comment(models.Model):
    """Creates a Comment DB model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return '"{body}..." on {post_title} by {username}'.format(body=self.body[:20],
                                                                  post_title=self.post.title,
                                                                  username=self.user.username)
