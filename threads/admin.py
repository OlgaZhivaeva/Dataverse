from django.contrib import admin
from .models import Thread, Accrual, ThreadAuthorMaterial


class ThreadAuthorMaterialInline(admin.TabularInline):
    model = ThreadAuthorMaterial
    extra = 1


class ThreadAuthorMaterialAdmin(admin.ModelAdmin):
    list_display = ('thread', 'author_contract', 'conducted_online')


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = (
        'article_number',
        'department',
        'start_at',
        'end_at',
        'conducted_online'
    )
    list_filter = (
        'department',
        'conducted_online'
    )
    search_fields = (
        'article_number',
        'department'
    )
    date_hierarchy = 'start_at'
    inlines = [ThreadAuthorMaterialInline]


@admin.register(Accrual)
class AccrualAdmin(admin.ModelAdmin):
    list_display = (
        'contract_type',
        'contract_id',
        'accruals_at',
        'amount',
        'calculation_details'
    )
    list_filter = (
        'contract_type',
        'accruals_at'
    )
    search_fields = (
        'comment',
    )
    date_hierarchy = 'accruals_at'
