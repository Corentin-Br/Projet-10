from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name.capitalize(),
            last_name=last_name.upper(),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='first name',
        max_length=50)
    last_name = models.CharField(
        verbose_name='last_name',
        max_length=50
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Contributor(models.Model):
    permissions_choices = [["perm", "permission_1"], ["not_perm", "permission_2"]]  # Placeholder

    user = models.ForeignKey(to=MyUser, on_delete=models.CASCADE, related_name='contributors')
    project = models.ForeignKey(to='Project', on_delete=models.CASCADE, related_name='contributors')
    permission = models.CharField(choices=permissions_choices, max_length=50)
    role = models.CharField(max_length=30)  # Placeholder


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=30)


class Issue(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=255)
    tag = models.CharField(max_length=30)
    priority = models.CharField(max_length=30)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='issues')
    author = models.ForeignKey(to=MyUser, on_delete=models.CASCADE, related_name='issues_written')
    assignee = models.ForeignKey(to=MyUser, on_delete=models.CASCADE, related_name='issues_assigned')
    created_time = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    description = models.CharField(max_length=255)
    author = models.ForeignKey(to=MyUser, on_delete=models.CASCADE, related_name='comments_written')
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now=True)
