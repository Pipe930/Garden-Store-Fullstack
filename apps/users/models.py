from typing import Tuple
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Class to create users
class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):

        #The user model is instantiated
        user = self.model(
            username = username,
            email = self.normalize_email(email),
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )

        user.set_password(password)
        user.save(using = self.db)

        return user

    # Method of creating a user
    def create_user(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    # Method of creating a superuser
    def create_superuser(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, True, True, **extra_fields)

# User Model
class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=20, blank=True, null=True, default="(without first name)")
    last_name = models.CharField(max_length=20, blank=True, null=True, default="(without last name)")
    date_joined = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    class Meta:
        db_table = "user"
        verbose_name = "user"
        verbose_name_plural = "users"

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def natural_key(self) -> Tuple[str]:
        return (self.username,)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

# Subscription Model
class Subscription(models.Model):

    id_subscription = models.BigAutoField(primary_key=True)
    created = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)
    mount = models.PositiveIntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:

        db_table = "subscriptions"
        verbose_name = "subscripcion"
        verbose_name_plural = "subscripciones"

    def __str__(self) -> str:
        return self.username

# Profile Model
class Profile(models.Model):

    id_profile = models.BigAutoField(primary_key=True)
    run = models.PositiveIntegerField()
    dv = models.CharField(max_length=1)
    phone = models.PositiveIntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:

        db_table = "profile"
        verbose_name = "profile"
        verbose_name_plural = "profiles"

    def __str__(self) -> str:
        return self.user.username

# Person Model
class Person(models.Model):

    id_person = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    run = models.PositiveIntegerField(unique=True)
    dv = models.CharField(max_length=1)
    phone = models.CharField(max_length=12, unique=True)

    class Meta:

        db_table = "person"
        verbose_name = "person"
        verbose_name_plural = "people"
