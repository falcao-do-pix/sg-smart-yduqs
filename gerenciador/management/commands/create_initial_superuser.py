import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Cria um superusuário padrão se nenhum existir, usando variáveis de ambiente.'

    def handle(self, *args, **options):
        User = get_user_model() # Obtém o seu modelo de usuário customizado (gerenciador.Usuario)
        
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not all([username, email, password]):
            self.stdout.write(self.style.ERROR(
                'As variáveis de ambiente DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, '
                'e DJANGO_SUPERUSER_PASSWORD devem ser definidas.'
            ))
            return

        # Verifica se o usuário já existe usando o USERNAME_FIELD do seu modelo
        # Para o seu modelo Usuario, o USERNAME_FIELD é 'matricula'
        # Se o admin que você está criando usa 'matricula' como username, isso está correto.
        # Se você quer que o admin use um campo 'username' tradicional, e seu modelo
        # não o tem, você precisaria ajustar aqui ou usar um modelo diferente para admin.
        # Assumindo que DJANGO_SUPERUSER_USERNAME será a matrícula do admin.
        
        # Para o modelo Usuario com USERNAME_FIELD = 'matricula':
        identifier_field = User.USERNAME_FIELD 
        if not User.objects.filter(**{identifier_field: username}).exists():
            try:
                User.objects.create_superuser(
                    # O método create_superuser do seu UsuarioManager espera:
                    # matricula, email, password
                    # Portanto, o 'username' da variável de ambiente será a 'matricula'
                    matricula=username, 
                    email=email, 
                    password=password
                )
                self.stdout.write(self.style.SUCCESS(f'Superusuário "{username}" criado com sucesso.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Erro ao criar superusuário "{username}": {e}'))
        else:
            self.stdout.write(self.style.WARNING(f'Superusuário "{username}" (matrícula) já existe.'))

