from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from djongo import models as djongo_models

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    _id = djongo_models.ObjectIdField()  # To match your MongoDB schema
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
