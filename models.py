import uuid
from django.db import models
from application.movie.user.models import User


class UserProfile(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    password = models.CharField(max_length=50, unique=False)

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "profile"
