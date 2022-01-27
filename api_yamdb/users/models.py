from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


USER_ROLE = "user"
MODERATOR_ROLE = "moderator"
ADMIN_ROLE = "admin"

ROLE_CHOICES = (
    (USER_ROLE, "Пользователь"),
    (MODERATOR_ROLE, "Модератор"),
    (ADMIN_ROLE, "Администратор"),
)


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password=None, **extra_fields):
        """Создание пользователя, проверка пароля."""

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        if password is None:
            user.set_unusable_password()
        else:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Создание суперюзера."""
        if password is None:
            raise TypeError("Superusers must have a password.")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(
            username=username, email=email, password=password, **extra_fields
        )


class CustomUser(AbstractUser):
    """Класс юзера с проверками."""

    email = models.EmailField(unique=True)
    bio = models.TextField("Биография", blank=True)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=USER_ROLE,
        verbose_name="Роль",
    )
    confirmation_code = models.CharField(max_length=128, null=True, blank=True)

    objects = CustomUserManager()

    @property
    def is_admin(self):
        """Проверка админа."""
        return self.role == ADMIN_ROLE or self.is_superuser

    @property
    def is_moderator(self):
        """Проверка модератора."""
        return self.role == MODERATOR_ROLE or self.is_staff

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
