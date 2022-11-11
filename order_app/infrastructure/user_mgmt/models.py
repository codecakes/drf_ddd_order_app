from django.db import models


class UserModel(models.Model):
    username = models.CharField(max_length=100, unique=True, null=False)
    password = models.CharField(max_length=100, null=False)


class Session(models.Model):
    """Token session to live till ttl expires."""

    token = models.BinaryField(null=False)
    ttl = models.DateTimeField(null=False, auto_now_add=False, auto_now=False)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=False)


