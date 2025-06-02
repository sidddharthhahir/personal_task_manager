from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Task
import urllib3
import json
import random

def get_motivational_quote():
    """Fetch a random motivational quote from API"""
    try:
        http = urllib3.PoolManager()
        response = http.request('GET', 'https://type.fit/api/quotes')
        quotes = json.loads(response.data.decode('utf-8'))
        if quotes:
            return random.choice(quotes)['text']
        return "Believe you can and you're halfway there."
    except:
        return "Believe you can and you're halfway there."

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@login_required
def task_list(request):
    status_filter = request.GET.get('status', 'all')
    tasks = Task.objects.filter(user=request.user)

    if status_filter == 'completed':
        tasks = tasks.filter(completed=True)
    elif status_filter == 'pending':
        tasks = tasks.filter(completed=False)

    quote = get_motivational_quote()

    context = {
        'tasks': tasks,
        'quote': quote,
        'status_filter': status_filter,
        'pending_count': Task.objects.filter(user=request.user, completed=False).count(),
        'completed_count': Task.objects.filter(user=request.user, completed=True).count(),
    }
    return render(request, 'tasks/task_list.html', context)

@login_required
def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        due_date = request.POST.get('due_date') or None

        if title:
            Task.objects.create(
                user=request.user,
                title=title,
                description=description,
                due_date=due_date
            )
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
        else:
            messages.error(request, 'Title is required!')

    return render(request, 'tasks/task_create.html')

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        task.title = request.POST.get('title', task.title)
        task.description = request.POST.get('description', task.description)
        task.completed = request.POST.get('completed') == 'on'
        task.due_date = request.POST.get('due_date') or None
        task.save()
        messages.success(request, 'Task updated successfully!')
        return redirect('task_list')

    return render(request, 'tasks/task_update.html', {'task': task})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')

    return render(request, 'tasks/task_delete.html', {'task': task})

@login_required
def toggle_task(request, pk):
    """AJAX endpoint to toggle task completion"""
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.completed = not task.completed
        task.save()
        return JsonResponse({
            'success': True,
            'completed': task.completed
        })
    return JsonResponse({'success': False})
