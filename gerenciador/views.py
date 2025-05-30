from rest_framework import viewsets, filters, serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
# from django_filters.rest_framework import DjangoFilterBackend
from .models import Aluno, Professor, Presenca
from .serializers import AlunoSerializer, ProfessorSerializer, PresencaSerializer, DisciplinaSerializer, CursoSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .constants import CURSOS, DISCIPLINAS 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def aluno_me(request):
    try:
        # Busca a instância de Aluno usando a chave primária (pk)
        # do usuário logado (request.user).
        aluno_instance = Aluno.objects.get(pk=request.user.pk)
        serializer = AlunoSerializer(aluno_instance)
        return Response(serializer.data)
    except Aluno.DoesNotExist:
        # Isso significa que o usuário logado não tem um perfil Aluno.
        return Response({'detail': 'Perfil de Aluno não encontrado para este usuário.'}, status=404)
    except Exception as e:
        # Captura outros erros inesperados.
        print(f"Erro em aluno_me: {e}")
        return Response({'detail': 'Erro interno ao buscar dados do aluno.'}, status=500)


class LoginPorMatriculaAPIView(APIView):
    def post(self, request):
        matricula = request.data.get("matricula")
        senha = request.data.get("senha")

        if not matricula or not senha:
            return Response({"detail": "Matrícula e senha são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        usuario = authenticate(request, matricula=matricula, password=senha)
        if usuario is not None:
            refresh = RefreshToken.for_user(usuario)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })
        return Response({"detail": "Credenciais inválidas."}, status=status.HTTP_401_UNAUTHORIZED)


class DisciplinaView(APIView):
    def get(self, request):
        serializer = DisciplinaSerializer(DISCIPLINAS, many=True)
        return Response(serializer.data)

class CursoView(APIView):
    def get(self, request):
        serializer = CursoSerializer(CURSOS, many=True)
        return Response(serializer.data)

# ViewSet para Aluno
class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar

# ViewSet para Professor
class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated]

# ViewSet para Presença
class PresencaViewSet(viewsets.ModelViewSet):
    queryset = Presenca.objects.all().order_by('-data')
    serializer_class = PresencaSerializer
