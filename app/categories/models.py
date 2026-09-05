from django.db import models


class ProductsCategoryModel(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'categories'
        indexes = [
            models.Index(fields=['title',]),
            models.Index(fields=['slug',]),
        ]