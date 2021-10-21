from django import db
from django.db import models
from core.models import TimeStamp
from users.models import User


class Post(TimeStamp):
    title = models.CharField(max_length=100, null=False)
    content = models.TextField(null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'posts'

