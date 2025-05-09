from django.db import models
from django.contrib.auth.models import AbstractUser


class DjangoAccountUser(AbstractUser):
    position = models.CharField(max_length=100, blank=True, verbose_name="Должность")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.username} ({self.position})"


class Teacher(models.Model):
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=100,
        blank=True
    )
    middle_name = models.CharField(
        verbose_name="Отчество",
        max_length=100,
        blank=True
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=100,
        blank=True
    )

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"