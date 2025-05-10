from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class AccrualQuerySet(models.QuerySet):

    def create_accrual(self, contract, accruals_at, comment="", calculation_details=None):

        contract_type = ContentType.objects.get_for_model(contract)
        amount = 'вычисляем значение на основе calculation_details'

        accrual = self.create(
            contract_type=contract_type,
            contract_id=contract.pk,
            accruals_at=accruals_at,
            amount=amount,
            comment=comment,
            calculation_details=calculation_details if calculation_details is not None else {}
        )
        return accrual


class Thread(models.Model):
    article_number = models.CharField(
        verbose_name="Артикул",
        max_length=255,
        unique=True
    )
    department = models.CharField(
        verbose_name="Подразделение",
        max_length=100
    )
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
    conducted_online = models.BooleanField(
        verbose_name="Проводится онлайн",
        default=False
    )

    contracts_with_royalties = models.ManyToManyField(
        'contracts.AuthorContract',
        verbose_name="Контракты с авторскими отчислениями",
        related_name='author_materials',
        blank=True,
        through='ThreadAuthorMaterial'
    )
    completed_at = models.DateTimeField(
        verbose_name="Дата завершения",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Поток"
        verbose_name_plural = "Потоки"
        ordering = ['-start_at']

    def __str__(self):
        return self.article_number


class ThreadAuthorMaterial(models.Model):
    thread = models.ForeignKey(
        Thread,
        verbose_name="Потоки по авторским контрактам",
        on_delete=models.CASCADE,
        related_name='author_contracts'
    )
    author_contract = models.ForeignKey(
        'contracts.AuthorContract',
        verbose_name="Авторские контракты по потокам",
        on_delete=models.CASCADE,
        related_name='threads'
    )
    class Meta:
        verbose_name = "Связь потока и авторского материала"
        verbose_name_plural = "Связи потоков и авторских материалов"

    def __str__(self):
        return f"Поток {self.thread.article_number} авторский контракт {self.author_contract.course_name}"


class Accrual(models.Model):
    contract_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name="Тип контракта",
        limit_choices_to={
            'model__in': ('authorcontract', 'presentercontract', 'externalcontract')
        }
    )
    contract_id = models.PositiveIntegerField()
    contract = GenericForeignKey(
        'contract_type',
        'contract_id'
    )
    accruals_at = models.DateTimeField(
        verbose_name="Дата начисления",
        null=True,
        blank=True
    )
    confirmed_at = models.DateTimeField(
        verbose_name="Дата подтверждения",
        null=True,
        blank=True
    )
    paid_out_at = models.DateTimeField(
        verbose_name="Дата выплаты",
        null=True,
        blank=True
    )
    amount = models.DecimalField(
        verbose_name="Сумма начисления",
        max_digits=10,
        decimal_places=2
    )
    comment = models.CharField(
        verbose_name="Комментарий",
        max_length=500,
        blank=True
    )

    calculation_details = models.JSONField(
        default=dict,
        verbose_name="Детали расчета",
        help_text="JSON-данные, использованные при расчете начисления",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Начисление по контракту {self.contract}"

    class Meta:
        verbose_name = "Начисление"
        verbose_name_plural = "Начисления"
        ordering = ['-accruals_at']

    objects = AccrualQuerySet.as_manager()
