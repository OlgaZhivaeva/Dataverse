from django.contrib import admin
from .models import DjangoAccountUser, Teacher


@admin.register(DjangoAccountUser)
class DjangoAccountUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'position',
        'first_name',
        'last_name',
        'email'
    )
    list_filter = (
        'is_staff',
        'is_active',
        'is_superuser',
        'position'
    )
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'position'
    )
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'position')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'last_name',
        'first_name',
        'middle_name',
        'get_courses'
    )
    search_fields = (
        'last_name',
        'first_name',
        'middle_name'
    )
    ordering = (
        'last_name',
        'first_name'
    )

    def get_courses(self, obj):
        return ", ".join([course.course_name for course in obj.author_materials.all()])
    get_courses.short_description = "Курсы"