from django.contrib import admin

from .models import Category, Genre, Title, Review, Comment


class CategoryAdmin(admin.ModelAdmin):
    """Описывает модель раздела редактирования категорий."""

    list_display = (
        "pk",
        "name",
        "slug",
    )


class GenreAdmin(admin.ModelAdmin):
    """Описыват модель раздела редактирования жанров"""

    list_display = ("pk", "name", "slug")


class TitleAdmin(admin.ModelAdmin):
    """Описыват модель раздела редактирования произведений"""

    list_display = (
        "pk",
        "name",
        "year",
        "description",
        "category",
    )
    search_fields = ("name",)


class ReviewAdmin(admin.ModelAdmin):
    """Описыват модель раздела редактирования отзывов"""

    list_display = (
        "pk",
        "text",
        "author",
        "score",
        "pub_date",
        "title",
    )
    search_fields = ("title",)


class CommentAdmin(admin.ModelAdmin):
    """Описыват модель раздела редактирования комментариев"""

    list_display = (
        "pk",
        "review",
        "text",
        "author",
        "pub_date",
    )
    search_fields = ("review",)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
