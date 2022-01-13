from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import SET_NULL, CASCADE

User = get_user_model()

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
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle'
    )

    def __str__(self) -> str:
        return self.name

# В этой модели будут связаны произведение(title_id)
# и жанры, к которым оно может относиться(genre_id)
class GenreTitle(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=CASCADE,
        related_name='titles',
        null=False,
        blank=False,
        verbose_name='Произведение'        
    )
    genre_id = models.ForeignKey(
        Genre,
        on_delete=CASCADE,
        related_name='genres',
        null=False,
        blank=False,
        verbose_name='Жанр'        
    )

    def __str__(self) -> str:
        return f' {self.genre_id}'


class Reviews(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviewer"
    )
    score = models.DecimalField(
        max_digits=1,
        decimal_places=0
    )
    pub_date = models.DateTimeField(
        "Дата оценки",
        auto_now_add=True
    )
    
class Comments(models.Model):
    review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name="review"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="commenter"
    )
    pub_date = models.DateTimeField(
        "Дата комментария",
        auto_now_add=True
    )
