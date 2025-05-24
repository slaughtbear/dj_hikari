from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout # Funciones para iniciar y cerrar sesión, y autenticar
from django.contrib.auth.models import User
from django.db import IntegrityError # Maneja errores de integridad de la base de datos
from django.contrib.auth.decorators import login_required


def signin(request):
    if request.method == 'GET': # Si el método de acceso a la ruta es GET:
        return render(request, 'authentication/login_page.html', { # 1. Se renderiza la página de inicio de sesión
            'form': AuthenticationForm # Con el formulario de Django Auth para autenticar un usuario
        })
    else: # Si el método de acceso a la ruta es POST:
        # 1. Se valida que las credenciales proporcionadas correspondan a un usuario en la base de datos
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None: # Si el usuario no existe
            return render(request, 'authentication/login_page.html', {  # 1. Se renderiza la página de inicio de sesión 
                'form': AuthenticationForm, # 2. Con el formulario de Django Auth para autenticar un usuario
                'error': 'Nombre de usuario o contraseña incorrectos'  # 3. Se pasa un mensaje de error para el usuario
            })
        else: # Si el usuario sí existe en la base de datos:
            login(request, user) # 1. Se inicia sesión con la cuenta del usuario
            return redirect('prueba') # 2. Y finalmente lo redirecciona a la página de sus proyectos
        

def signup(request): # Vista para registrar un usuario
    if request.method == 'GET': # Si el método de acceso a la ruta es GET:
        return render(request, 'authentication/register_page.html', { # 1. Se renderiza la página de registro
            'form': UserCreationForm # Con el formulario de Django Auth para crear un usuario 
        })
    else: # Si el método de acceso a la ruta es POST:
        # 1. Se verifica que las contraseñas que registró el usuario coincidan
        if request.POST['password1'] == request.POST['password2']: # Si coinciden:
            try: # 2. Se usa un bloque de prueba para crear su usuario
                # 3. Con el método create_user() del modelo User de Django se registran los datos ingresadas
                user = User.objects.create_user(
                    username=request.POST['username'], # Nombre de usuario
                    password=request.POST['password1'] # Contraseña
                )
                user.save() # 4. Se guarda el usuario en la base de datos
                login(request, user) # 5. Se inicia sesión con la cuenta del usuario creado
                return redirect('signin') # 6. Y finalmente lo redirecciona a una página
            except IntegrityError: # Si ocurre un error al intentar crear el usuario:
                return render(request, 'authentication/register_page.html', { # 1. Se renderiza de nuevo la página de registro
                    'form': UserCreationForm, # 2. Formulario de Django Auth para crear un usuario
                    'error': 'El usuario ya existe.', # 3. Se pasa un mensaje de error para el usuario
                })
        else: # Si las contraseñas no coinciden:
             return render(request, 'authentication/register_page.html', { # 1. Se renderiza de nuevo la página de registro
            'form': UserCreationForm, # 2. Formulario de Django Auth para crear un usuario
            'error': 'Las contraseñas no coinciden.' # 3. Mensaje de error para el usuario
            })
        

@login_required
def signout(request): # Vista para cerrar sesión
    logout(request) # 1. Se cierra la sesión del usuario autenticado
    return redirect('#') # 2. Se redirecciona a una página