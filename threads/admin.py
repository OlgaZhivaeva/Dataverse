from django.contrib import admin
from .models import Thread, Accrual


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = (
        'article_number',
        'department',
        'start_at',
        'end_at',
        'online_form',
        'full_time_form'
    )
    list_filter = (
        'department',
        'online_form',
        'full_time_form'
    )
    search_fields = (
        'article_number',
        'department'
    )
    date_hierarchy = 'start_at'
    filter_horizontal = ('author_materials',)


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
