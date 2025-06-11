from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from .models import Quarto, Reserva
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def is_gerente(user):
    return user.groups.filter(name='Gerente').exists()

def is_atendente(user):
    return user.groups.filter(name='Atendente').exists()


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('password')
        user = authenticate(request, username=username, password=senha)
        if user:
            login(request, user)
            if is_gerente(user):
                return redirect('dashboard_gerente')
            elif is_atendente(user):
                return redirect('dashboard_atendente')
            else:
                messages.error(request, 'Usuário sem grupo definido.')
                logout(request)
                return redirect('login')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')



@login_required
@user_passes_test(is_gerente)
def dashboard_gerente(request):
    return render(request, 'dashboard_gerente.html')

@login_required
@user_passes_test(is_atendente)
def dashboard_atendente(request):
    return render(request, 'dashboard_atendente.html')


@login_required
@user_passes_test(is_gerente)
def cadastrar_quarto(request):
    if request.method == "POST":
        numero = request.POST.get('numero')
        tipo = request.POST.get('tipo')
        capacidade = request.POST.get('capacidade')

        if Quarto.objects.filter(numero=numero).exists():
            messages.error(request, f"O quarto número {numero} já está cadastrado.")
            return render(request, 'cadastrar_quarto.html')


        Quarto.objects.create(numero=numero, tipo=tipo, capacidade=capacidade)
        messages.success(request, "Quarto cadastrado com sucesso!")
        return redirect('listar_quartos')

    return render(request, 'cadastrar_quarto.html')


@login_required
@user_passes_test(is_gerente)
def listar_quartos(request):
    
    quartos = Quarto.objects.all()
    
    
    user_role = 'gerente' 

    context = {
        'quartos': quartos,
        'user_role': user_role,
    }
    return render(request, 'listar_quartos.html', context)

@login_required
def listar_quartos_disponiveis(request):
    quartos = Quarto.objects.filter(status='Disponível')
    
    user_role = None
    if request.user.groups.filter(name='Gerente').exists():
        user_role = 'gerente'
    elif request.user.groups.filter(name='Atendente').exists():
        user_role = 'atendente'

    return render(request, 'listar_quartos_disponiveis.html', {
        'quartos': quartos,
        'user_role': user_role
    })

@login_required
def reservar_quarto(request, quarto_id):
    quarto = get_object_or_404(Quarto, id=quarto_id)

    if quarto.status != 'Disponível':
        messages.error(request, 'Quarto não disponível para reserva.')
        return redirect('listar_quartos_disponiveis')

    if request.method == 'POST':
        nome_hospede = request.POST.get('nome_hospede')
        Reserva.objects.create(
            quarto=quarto,
            hospede_nome=nome_hospede,
            reservado_por=request.user
        )
        quarto.status = 'Reservado'
        quarto.save()
        messages.success(request, f'Quarto {quarto.numero} reservado para {nome_hospede}.')
        return redirect('listar_quartos_disponiveis')

    return render(request, 'reservar_quarto.html', {'quarto': quarto})


@login_required
@user_passes_test(is_gerente)
def cadastrar_colaborador(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Usuário já existe.')
            return redirect('cadastrar_colaborador')

        user = User.objects.create_user(username=username, password=password)
        atendente_group = Group.objects.get(name='Atendente')
        user.groups.add(atendente_group)
        messages.success(request, f'Colaborador {username} cadastrado como Atendente.')
        return redirect('dashboard_gerente')

    return render(request, 'cadastrar_colaborador.html')
def registrar_usuario(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = UserCreationForm()
        return render(request, 'registro.html', {'form': form})

@login_required
def dashboard_redirect(request):
    if request.user.is_staff:
        return redirect('dashboard_gerente')
    else:
        return redirect('dashboard_atendente')