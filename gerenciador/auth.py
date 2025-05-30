from django.contrib.auth.backends import BaseBackend
from gerenciador.models import Usuario

class MatriculaAuthBackend(BaseBackend):
    """
    Autentica usando matrícula e senha padrão do Django.
    """
    def authenticate(self, request, matricula=None, password=None, **kwargs):
        # Fallback: Django usa 'username' como USERNAME_FIELD
        if matricula is None:
            matricula = kwargs.get('username')

        if not matricula or not password:
            return None

        try:
            usuario = Usuario.objects.get(matricula=matricula)
        except Usuario.DoesNotExist:
            return None

        if usuario.check_password(password):
            return usuario
        return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
