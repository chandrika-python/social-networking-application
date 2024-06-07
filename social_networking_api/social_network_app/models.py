from django.db import models
from django.contrib.auth.models import AbstractUser


class UsersModel(AbstractUser):
    username = models.EmailField(unique=True)


class FriendRequestModel(models.Model):
    from_user = models.ForeignKey(UsersModel, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(UsersModel, related_name='received_requests', on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')))

    class Meta:
        unique_together = ('from_user', 'to_user')