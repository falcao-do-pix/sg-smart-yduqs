from rest_framework import serializers
from .models import Usuario, Aluno, Professor, Presenca # CURSOS, DISCIPLINAS (Se forem usados aqui)
# from django.contrib.auth.hashers import make_password # Não é mais necessário aqui para create/update de Usuario
from django.utils import timezone
from .constants import CURSOS, DISCIPLINAS # Adicionado se CURSOS e DISCIPLINAS forem realmente de .constants

class CursoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nome = serializers.CharField(max_length=100)

class DisciplinaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nome = serializers.CharField(max_length=100)
    # Se 'cursos' em DisciplinaSerializer deve vir da constante CURSOS:
    # cursos = serializers.SerializerMethodField()
    # def get_cursos(self, obj):
    #     # Lógica para associar cursos a disciplinas se necessário,
    #     # ou ajustar conforme a estrutura de dados de DISCIPLINAS
    #     return [] # Placeholder

class UsuarioBaseSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = Usuario
        fields = ['id', 'matricula', 'nome', 'email', 'senha', 'data_criacao']
        read_only_fields = ['id', 'data_criacao']

    def create(self, validated_data):
        """
        Cria e retorna uma nova instância de Usuário (ou suas subclasses),
        garantindo que o método 'create_user' do manager seja chamado
        para criptografar a senha corretamente.
        """
        # Pega a senha e remove do dict principal
        password = validated_data.pop('senha')
        
        # Pega os campos esperados por create_user
        matricula = validated_data.pop('matricula')
        email = validated_data.pop('email')
        
        # O que sobrar em validated_data (como 'nome', 'curso', etc.)
        # será passado como **extra_fields para create_user.

        # Obtém o manager do modelo (seja Usuario ou Aluno)
        user_manager = self.Meta.model.objects

        # Chama create_user explicitamente.
        # Ele lida com a criptografia da senha e salva o usuário.
        usuario = user_manager.create_user(
            matricula=matricula,
            email=email,
            password=password,
            **validated_data  # Passa os campos restantes (nome, curso, etc.)
        )
        return usuario

    def update(self, instance, validated_data):
        """
        Atualiza e retorna uma instância de Usuário existente.
        Se uma nova senha for fornecida, usa set_password().
        """
        password_plain = validated_data.pop('senha', None)
        if password_plain:
            instance.set_password(password_plain)
            # A instância será salva por super().update()

        # Chama o update original para lidar com outros campos
        return super().update(instance, validated_data)

# Serializer para Aluno
class AlunoSerializer(UsuarioBaseSerializer):
    class Meta(UsuarioBaseSerializer.Meta):
        model = Aluno
        # Adiciona 'curso' aos campos herdados.
        # Garante que 'senha' (write_only) e outros campos de UsuarioBaseSerializer.Meta.fields sejam incluídos.
        fields = list(UsuarioBaseSerializer.Meta.fields) + ['curso']


# Serializer para Professor
class ProfessorSerializer(UsuarioBaseSerializer):
    class Meta(UsuarioBaseSerializer.Meta):
        model = Professor
        fields = list(UsuarioBaseSerializer.Meta.fields) # Garante que os campos sejam copiados


# Serializer para Presença
class PresencaSerializer(serializers.ModelSerializer):
    # matricula = serializers.CharField() # O ModelSerializer já cria isso a partir do campo do modelo.
                                        # Se precisar de validação customizada, pode sobrescrever.

    class Meta:
        model = Presenca
        fields = ['id', 'matricula', 'data', 'hora_entrada', 'hora_saida', 'status']
        read_only_fields = ['data'] # 'data' é preenchida automaticamente no save do modelo ou no create do serializer
        extra_kwargs = {
            'status': {'required': False, 'allow_null': True}, # Permitir null se o default for None
            'hora_entrada': {'required': False, 'allow_null': True},
            'hora_saida': {'required': False, 'allow_null': True},
        }
    
    # Removido perform_create, pois não estava sendo usado corretamente.
    # O método create é o local para essa lógica.

    def validate_matricula(self, value):
        if len(value) > 20:
            raise serializers.ValidationError("A matrícula não pode ter mais que 20 caracteres.")
        if not Aluno.objects.filter(matricula=value).exists(): # ou Usuario, dependendo de quem pode ter presença
            raise serializers.ValidationError("Aluno com essa matrícula não existe.")
        return value

    def create(self, validated_data):
        data_hoje = timezone.now().date()
        matricula = validated_data['matricula']

        # Tenta buscar ou criar uma presença para a matrícula e o dia atual
        # Usar update_or_create é mais idiomático para essa lógica.
        instance, created = Presenca.objects.update_or_create(
            matricula=matricula,
            data=data_hoje,
            defaults={
                'hora_entrada': validated_data.get('hora_entrada'),
                'hora_saida': validated_data.get('hora_saida'),
                'status': validated_data.get('status')
            }
        )
        # Se não foi criado (foi atualizado), e você quer sobrescrever apenas se valores forem fornecidos:
        if not created:
            if 'hora_entrada' in validated_data:
                instance.hora_entrada = validated_data.get('hora_entrada', instance.hora_entrada)
            if 'hora_saida' in validated_data:
                instance.hora_saida = validated_data.get('hora_saida', instance.hora_saida)
            if 'status' in validated_data: # Apenas atualiza status se fornecido
                instance.status = validated_data.get('status', instance.status)
            instance.save()
        elif instance.status is None and 'status' not in validated_data: # Se for novo e status não veio
            instance.status = None # Ou algum default se preferir, mas o modelo já tem default=None

        return instance


    def update(self, instance, validated_data):
        # A lógica de update_or_create no create já cobre muitos casos.
        # Se o update for chamado diretamente (ex: PUT para um registro existente),
        # esta lógica será usada.

        instance.hora_entrada = validated_data.get('hora_entrada', instance.hora_entrada)
        instance.hora_saida = validated_data.get('hora_saida', instance.hora_saida)

        # Lógica para status: Só permite definir uma vez ou se for para o mesmo valor.
        novo_status = validated_data.get('status')
        if novo_status is not None: # Se um novo status foi fornecido
            if instance.status is not None and novo_status != instance.status:
                 # Se já existe um status e o novo é diferente, erro.
                 # (A menos que você queira permitir a alteração, então remova esta condição)
                raise serializers.ValidationError({"status": "Status já foi definido e não pode ser alterado para um valor diferente."})
            instance.status = novo_status
        
        instance.save()
        return instance

