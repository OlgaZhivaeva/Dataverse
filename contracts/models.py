from django.db import models
from django.conf import settings
from accounts.models import Teacher


class BaseContract(models.Model):
    start_at = models.DateTimeField(
        verbose_name="Дата начала",
        null=True,
        blank=True
    )
    end_at = models.DateTimeField(
        verbose_name="Дата окончания",
        null=True,
        blank=True
    )
    currency = models.CharField(
        verbose_name="Валюта",
        max_length=3,
        default='руб'
    )
    comment = models.CharField(
        verbose_name="Комментарий",
        max_length=500,
        blank=True
    )
    responsible_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Ответственный менеджер",
        on_delete=models.CASCADE,
        related_name='contracts',
        limit_choices_to={'position': 'Менеджер'}
    )

    def __str__(self):
        return f"Contract ID {self.pk}"


class AuthorContract(BaseContract):
    counterparty = models.ForeignKey(
        Teacher,
        verbose_name="Автор курса",
        related_name='author_materials',
        on_delete=models.RESTRICT
    )
    course_name = models.CharField(
        verbose_name="Название курса",
        max_length=100,
        blank=True
    )
    commission_rate = models.DecimalField(
        verbose_name="Комиссионный процент",
        max_digits=5,
        decimal_places=2
    )
    calculation_method = models.CharField(
        verbose_name="Метод расчета",
        max_length=100,
        blank=True
    )

    class Meta:
        verbose_name = "Авторский контракт"
        verbose_name_plural = "Авторские контракты"

    def __str__(self):
        return f"Contract ID {self.pk} {self.course_name}"


class PresenterContract(BaseContract):
    counterparty = models.ForeignKey(
        Teacher,
        verbose_name="Ведущий потока",
        on_delete=models.RESTRICT
    )
    hourly_rate = models.DecimalField(
        verbose_name="Почасовой рейт",
        max_digits=10,
        decimal_places=2
    )
    thread = models.ForeignKey(
        'threads.Thread',
        verbose_name="Поток",
        on_delete=models.RESTRICT
    )
    calculation_method = models.CharField(
        verbose_name="Метод расчета",
        max_length=100,
        blank=True
    )

    class Meta:
        verbose_name = "Контракт с ведущим"
        verbose_name_plural = "Контракты с ведущими"


class Contractor(models.Model):
    name = models.CharField(
        verbose_name="Подрядчик",
        max_length=200,
        blank=True
    )
    description = models.CharField(
        verbose_name="Описание",
        max_length=500,
        blank=True
    )

    class Meta:
        verbose_name = "Подрядчик"
        verbose_name_plural = "Подрядчики"

    def __str__(self):
        return self.name


class ExternalContract(BaseContract):
    counterparty = models.ForeignKey(
        Contractor,
        verbose_name="Контрагент",
        on_delete=models.RESTRICT
    )
    contract_amount = models.DecimalField(
        verbose_name="Сумма контракта",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Внешний контракт"
        verbose_name_plural = "Внешние контракты"
