from django.db import models
from django.db.models.deletion import SET_NULL, CASCADE

from users.models import CustomUser


SCORES = [(i, i) for i in range(1, 11)]


class Category(models.Model):
    name = models.CharField(
        max_length=50, verbose_name="Категория произведения"
    )
    slug = models.SlugField(unique=True, verbose_name="URL категории")

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50, verbose_name="Жанры")
    slug = models.SlugField(unique=True, verbose_name="URL жанра")

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200, verbose_name="Название произведения"
    )
    year = models.IntegerField(verbose_name="Дата создания")

    description = models.TextField(
        verbose_name="Описание произведения",
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=SET_NULL,
        related_name="titles",
        null=True,
        blank=True,
        verbose_name="Категория",
    )
    genre = models.ManyToManyField(Genre, through="GenreTitle")

    class Meta:
        ordering = ["-pk"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(year__gte=1000),
                name="year_must_be_gte_1000",
            )
        ]

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=CASCADE,
        related_name="genres",
        verbose_name="Произведение",
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=CASCADE,
        related_name="titles",
        verbose_name="Жанр",
    )

    def __str__(self):
        return self.genre


class Review(models.Model):
    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва",
    )
    score = models.IntegerField(choices=SCORES, verbose_name="Оценка")
    pub_date = models.DateTimeField("Дата оценки", auto_now_add=True)
    title = models.ForeignKey(
        Title,
        on_delete=CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )

    class Meta:
        ordering = ["-pk"]
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"],
                name="unique_review"
            )
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв",
    )
    text = models.TextField(verbose_name="Комментарий")
    author = models.ForeignKey(
        CustomUser,
        on_delete=CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата комментария"
    )

    class Meta:
        ordering = ["-pk"]

    def __str__(self):
        return self.text[:15]
