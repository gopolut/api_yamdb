from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password=None, **extra_fields):
        """Создание пользователя, проверка пароля. """

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        if password is None:
            user.set_unusable_password()
        else:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Создание суперюзера. """
        if password is None:
            raise TypeError('Superusers must have a password.')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(
            username=username,
            email=email,
            password=password,
            **extra_fields
        )


class CustomUser(AbstractUser):
    """Класс юзера с проверками."""
    email = models.EmailField(unique=True)
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name='Роль'
    )
    confirmation_code = models.CharField(
        max_length=128, null=True, blank=True
    )

    objects = CustomUserManager()

    def is_admin(self):
        """Проверка админа."""
        return self.role == 'admin' or self.is_superuser

    def is_moderator(self):
        """Проверка модератора."""
        return self.role == 'moderator' or self.is_staff

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
