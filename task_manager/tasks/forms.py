from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task title...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter task description...'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }

class TaskFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('all', 'All Tasks'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        initial='all',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
