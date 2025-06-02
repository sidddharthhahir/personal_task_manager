from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Task
import requests
from django.http import JsonResponse

def get_motivational_quote():
    try:
        response = requests.get('https://type.fit/api/quotes', timeout=3)
        if response.status_code == 200:
            quotes = response.json()
            import random
            quote = random.choice(quotes)
            return quote.get('text', '')
    except Exception:
        pass
    return "Stay motivated!"

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
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
            return redirect('task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    quote = get_motivational_quote()
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'quote': quote})

@login_required
def task_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST.get('description', '')
        due_date = request.POST.get('due_date') or None
        Task.objects.create(user=request.user, title=title, description=description, due_date=due_date)
        return redirect('task_list')
    return render(request, 'tasks/task_create.html')

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST.get('description', '')
        task.completed = request.POST.get('completed', '') == 'on'
        task.due_date = request.POST.get('due_date') or None
        task.save()
        return redirect('task_list')
    return render(request, 'tasks/task_update.html', {'task': task})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_delete.html', {'task': task})
def toggle_task(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.completed = not task.completed
        task.save()
        return JsonResponse({'success': True, 'completed': task.completed})
    return JsonResponse({'success': False})