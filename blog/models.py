from django.db import models
from django.utils import timezone
# To set author i.e. user from User Table we need to add below import
from django.contrib.auth.models import User
from django.urls import reverse
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)  # possible values - auto_now = True , auto_now_add = True, default
    # need author having relation with Users table in Django Database
    author = models.ForeignKey(User,on_delete = models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})