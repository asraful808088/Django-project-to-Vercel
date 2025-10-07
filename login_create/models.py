from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, phone, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not phone:
            raise ValueError('The Phone field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, phone, username, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    username = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=30, unique=True)
    account_type = models.CharField(max_length=30, blank=True)
    password = models.CharField(max_length=300, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email", "phone", "first_name", "last_name", "account_type","password"]
    def has_module_perms(self, app_label):
        return True
    def has_perm(self, perm, obj=None):
         return True
    def __str__(self):
        return self.email
