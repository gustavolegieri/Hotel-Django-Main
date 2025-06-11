from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import registrar_usuario
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView

@login_required
def dashboard_redirect(request):
    if request.user.is_staff:
        return redirect('dashboard_gerente')
    else:
        return redirect('dashboard_atendente')


urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('dashboard/gerente/', views.dashboard_gerente, name='dashboard_gerente'),
    path('dashboard/atendente/', views.dashboard_atendente, name='dashboard_atendente'),

    path('quartos/cadastrar/', views.cadastrar_quarto, name='cadastrar_quarto'),
    path('quartos/listar/', views.listar_quartos, name='listar_quartos'),

    path('quartos/disponiveis/', views.listar_quartos_disponiveis, name='listar_quartos_disponiveis'),
    path('quartos/reservar/<int:quarto_id>/', views.reservar_quarto, name='reservar_quarto'),

    path('colaboradores/cadastrar/', views.cadastrar_colaborador, name='cadastrar_colaborador'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registrar/', registrar_usuario, name='registrar'),
    path('dashboard/', dashboard_redirect, name='dashboard'),
]
