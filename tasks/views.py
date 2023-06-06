from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .forms import TaskForm, CumpleForm
from .models import Task, Cumple, SharedTask
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        print('enviando formulario')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Usuario ya existente'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Las contraseñas no coinciden'
        })

    return render(request, 'signup.html', {
        'form': UserCreationForm
    })


@login_required
def tasks(request):
    pending_tasks = Task.objects.filter(users=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'pending_tasks': pending_tasks})

@login_required
def tasks_completed(request):
    completed_tasks = Task.objects.filter(users=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'completed_tasks': completed_tasks})


@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.save()
            new_task.users.add(request.user)
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                "error": 'Error al crear la tarea'
            })


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, users=request.user)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
        else:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': "Error actualizando Tareas"})


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, users=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, users=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Nombre de usuario o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('home')


@login_required
def cumple(request):
    cumple_list = Cumple.objects.filter(users=request.user)
    context = {
        'cumple_list': cumple_list
    }
    return render(request, 'cumple.html', context)

@login_required
def agregarCumple(request):
    if request.method == 'POST':
        form = CumpleForm(request.POST)
        if form.is_valid():
            cumple = form.save(commit=False)
            cumple.save()
            cumple.users.set([request.user])  # Utiliza el método set() para asignar los usuarios
            return redirect('cumple')
    else:
        form = CumpleForm()
    context = {
        'form': form
    }
    return render(request, 'agregarCumple.html', context)



@login_required
def delete_cumple(request, cumple_id):
    cumple = get_object_or_404(Cumple, id=cumple_id, users=request.user)
    if request.method == 'POST':
        cumple.delete()
        return redirect('cumple')
    context = {
        'cumple': cumple
    }
    return render(request, 'delete_cumple.html', context)



@login_required
def admin_view(request):
    if request.user.is_superuser:  # Verificar si el usuario es un superusuario o administrador
        users = User.objects.all()  # Obtener todos los usuarios
        return render(request, 'admin_view.html', {'users': users})
    else:
        return redirect('home')
    
@login_required
def shared_tasks(request):
    shared_tasks = SharedTask.objects.filter(users=request.user).values_list('task', flat=True)
    pending_tasks = Task.objects.filter(pk__in=shared_tasks, datecompleted__isnull=True).distinct()
    return render(request, 'shared_tasks.html', {'pending_tasks': pending_tasks})

