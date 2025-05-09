from django.contrib import admin
from .models import AuthorContract, PresenterContract, Contractor, ExternalContract
from threads.models import Accrual
from django.contrib.contenttypes.admin import GenericTabularInline


class AccrualInline(GenericTabularInline):
    model = Accrual
    ct_field = "contract_type"
    ct_fk_field = "contract_id"
    extra = 1


class BaseContractAdmin(admin.ModelAdmin):
    list_display = (
        'start_at',
        'end_at',
        'responsible_manager'
    )
    list_filter = (
        'responsible_manager',
    )
    search_fields = (
        'comment',
    )
    date_hierarchy = 'start_at'


@admin.register(AuthorContract)
class AuthorContractAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'counterparty',
        'course_name',
        'commission_rate',
        'calculation_method',
        *BaseContractAdmin.list_display
    )
    list_filter = (
        'counterparty',
        *BaseContractAdmin.list_filter
    )
    search_fields = (
        'calculation_method',
        'counterparty__last_name',
        'counterparty__first_name',
        'counterparty__middle_name'
    )
    fields = (
        ('counterparty', 'course_name', 'commission_rate', 'calculation_method'),
        ('start_at', 'end_at', 'comment', 'responsible_manager')
    )
    inlines = [AccrualInline]


@admin.register(PresenterContract)
class PresenterContractAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'counterparty',
        'hourly_rate',
        'thread',
        'calculation_method',
        *BaseContractAdmin.list_display
    )
    list_filter = (
        'thread',
        'counterparty',
        *BaseContractAdmin.list_filter
    )
    search_fields = (
        'calculation_method',
        'thread__article_number',
        'counterparty__last_name',
        'counterparty__first_name',
        'counterparty__middle_name'
    )
    fields = (
        ('counterparty', 'hourly_rate', 'thread', 'calculation_method'),
        ('start_at', 'end_at', 'comment', 'responsible_manager')
    )
    inlines = [AccrualInline]


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description'
    )
    search_fields = (
        'name',
        'description'
    )


@admin.register(ExternalContract)
class ExternalContractAdmin(BaseContractAdmin):
    list_display = (
        'id',
        'counterparty',
        'contract_amount',
        *BaseContractAdmin.list_display
    )
    list_filter = (
        'counterparty',
        *BaseContractAdmin.list_filter
    )
    search_fields = (
        'counterparty__name',
        'counterparty__description'
    )
    fields = (
        ('counterparty', 'contract_amount'),
        ('start_at', 'end_at', 'comment', 'responsible_manager')
    )
    inlines = [AccrualInline]
