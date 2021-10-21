from django.db import models

from core.models import TimeStamp


class User(TimeStamp):
    name     = models.CharField(max_length = 50)
    email    = models.EmailField(max_length = 50, unique = True)
    password = models.CharField(max_length = 500)
    
    class Meta:
        db_table = "users"