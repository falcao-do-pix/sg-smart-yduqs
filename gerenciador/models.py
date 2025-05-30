from django.db import models
from django.contrib.auth.models import Group, Permission, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from .constants import CURSOS, DISCIPLINAS

class UsuarioManager(BaseUserManager):
    def create_user(self, matricula, email, password=None, **extra_fields):
        if not matricula:
            raise ValueError("A matrícula é obrigatória.")
        if not email:
            raise ValueError("O email é obrigatório.")

        email = self.normalize_email(email)
        user = self.model(matricula=matricula, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, matricula, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(matricula, email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    matricula = models.CharField(max_length=20, unique=True)
    nome = models.CharField(
        max_length=255,
        null=True, blank=True,
        help_text="Somente para compatibilidade com usuários antigos. Não será usado para novos registros."
    )
    email = models.EmailField(unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name="usuarios", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="usuarios_perms", blank=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'matricula'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

        

CURSO_CHOICES = [(curso["id"], curso["nome"]) for curso in CURSOS]


class Aluno(Usuario):
    curso = models.CharField(
        max_length=100,
        choices=CURSO_CHOICES,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Aluno: {self.nome} - {self.matricula}"

    
    
class Professor(Usuario):
    def __str__(self):
        return f"Professor: {self.nome} ({self.matricula})"



class Presenca(models.Model):
    STATUS_CHOICES = [
        ('P', 'Presente'),
        ('F', 'Faltou'),
    ]

    matricula = models.CharField(max_length=20, unique=True)
    data = models.DateField(editable=False)  # Preenchida automaticamente
    hora_entrada = models.TimeField(null=False, blank=True)
    hora_saida = models.TimeField(null=False, blank=True)
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        null=False,
        blank=True,
        default=None
    )

    def save(self, *args, **kwargs):
        if not self.data:
            self.data = timezone.localdate()  # Usa data atual local
        super().save(*args, **kwargs)

    def __str__(self):
        status = self.get_status_display() if self.status else "Sem status"
        return f"{self.matricula} - {self.data} - {status}"

    class Meta:
        unique_together = ('matricula', 'data')  # Garante um único registro diário por aluno
        verbose_name = "Presença"