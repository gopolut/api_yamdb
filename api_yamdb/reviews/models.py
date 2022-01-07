from django.db import models
from django.db.models.deletion import SET_NULL, CASCADE


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Категории контента'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='URL категории'
    )

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Жанры'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='URL жанра'
    )

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название произведения'
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Дата создания'
    )
    category = models.ForeignKey(
        Category,
        on_delete=SET_NULL,
        related_name='titles',
        null=True,
        blank=True,
        verbose_name='Категория'
    )
    # genre = models.ManyToManyField(
    #     Genre,
    #     through='GenreTitle'
    # )

    def __str__(self) -> str:
        return self.name

# В этой модели будут связаны произведение(title_id)
# и жанры, к которым оно может относиться(genre_id)
class GenreTitle(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=CASCADE,
        related_name='title',
        null=False,
        blank=False,
        verbose_name='Произведение'        
    )
    genre_id = models.ForeignKey(
        Genre,
        on_delete=CASCADE,
        related_name='genre',
        null=False,
        blank=False,
        verbose_name='Жанр'        
    )

    def __str__(self) -> str:
        return f' {self.genre_id}'
