
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, phone=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            phone_number=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, phone=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('roles', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(
            username=username,
            email=email,
            phone=phone,
            password=password,
            **extra_fields
        )


class CustomUser(AbstractBaseUser):
    USER_ROLES = (
        ('admin', '管理员'),
        ('user', '普通用户'),
    )
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    roles = models.CharField(choices=USER_ROLES, max_length=15, default='user')
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 't_custom_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True







