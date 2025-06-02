from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'completed', 'created_at', 'due_date']
    list_filter = ['completed', 'created_at', 'due_date']
    search_fields = ['title', 'description']
    list_editable = ['completed']
