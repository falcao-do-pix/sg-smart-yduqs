from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.register_view, name='cadastro_aluno'),
    path('painel/', views.painel_aluno, name='painel_aluno'),
    path('editar-perfil/', views.editar_perfil_view, name='editar_perfil'),
    path('selecionar-curso/', views.selecionar_curso_view, name='selecionar_curso'),
    path('api/buscar-curos/', views.buscar_cursos, name='buscar_cursos'),
    path('login/', views.login_view, name='login_aluno'),
    path('logout/', views.logout_view, name='logout_aluno'),
]
