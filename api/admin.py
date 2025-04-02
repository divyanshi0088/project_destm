from django.contrib import admin

from django.contrib import admin
from .models import User, Teacher, Student

# Custom admin for User model
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'username')
    list_filter = ('role', 'is_active', 'is_staff')

admin.site.register(User, UserAdmin)

# Admin for Teacher model
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__email', 'user__username')
    list_filter = ('user__role',)

admin.site.register(Teacher, TeacherAdmin)

# Admin for Student model
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'teacher')
    search_fields = ('user__email', 'user__username')
    list_filter = ('teacher',)

admin.site.register(Student, StudentAdmin)
