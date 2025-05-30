from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlunoViewSet, ProfessorViewSet, PresencaViewSet, DisciplinaView, CursoView, LoginPorMatriculaAPIView, aluno_me
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Criando um router para registrar os ViewSets automaticamente
router = DefaultRouter()
router.register(r'alunos', AlunoViewSet)
router.register(r'professores', ProfessorViewSet)
router.register(r'presencas', PresencaViewSet)


urlpatterns = [
    path('api/', include(router.urls)),  # Inclui todas as rotas registradas
    path('api/disciplinas/', DisciplinaView.as_view(), name='lista-disciplina'),
    path('api/cursos/', CursoView.as_view(), name='lista-cursos'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login-matricula/', LoginPorMatriculaAPIView.as_view(), name='login_matricula'),
    path('api/aluno/me/', aluno_me, name='aluno_me'),
]