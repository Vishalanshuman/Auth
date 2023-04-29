from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.


class CustomUser(BaseUserManager):
    def create_user(self, username, password,**extra_fields):
        
        user = self.model(
            username = username,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)


        if extra_fields.get('is_staff')is not True:
            raise ValueError("is_staff need to be True for Superuser.")
        if extra_fields.get('is_superuser')is not True:
            raise ValueError("is_superuser need to be True for Superuser.")

        user = self.create_user(username=username, password=password, **extra_fields)
        return user
 

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200, null=True)
    mobile = models.CharField(max_length=10, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUser()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email




