from django.contrib import admin
from .models import Teacher, Feedback

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'email')
    search_fields = ('name',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('student', 'teacher', 'rating', 'created_at')
    list_filter = ('rating', 'teacher', 'created_at')
