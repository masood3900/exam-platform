from django.db import models

# Create your models here.
class Department(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    code = models.CharField(
        max_length=20,
        unique=True
    )
    is_active = models.BooleanField(
    default=True,
    )
    created_at = models.DateTimeField(

        auto_now_add=True,
    )
    class Meta:
        ordering = ["name"]
        verbose_name = "واحدهای آموزشی"
        verbose_name_plural = "واحدهای آموزشی"
    def __str__(self):
        return self.name