# Generated by Django 5.1.7 on 2025-05-22 23:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('matricula', models.CharField(max_length=20, unique=True)),
                ('nome', models.CharField(blank=True, help_text='Somente para compatibilidade com usuários antigos. Não será usado para novos registros.', max_length=255, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, related_name='usuarios', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='usuarios_perms', to='auth.permission')),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
            },
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('curso', models.CharField(blank=True, choices=[(1, 'Engenharia'), (2, 'Ciência da Computação'), (3, 'Tecnologia da Informação'), (4, 'Letras'), (5, 'Advocacia'), (6, 'Artes'), (7, 'Engenharia da Computação')], max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('gerenciador.usuario',),
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('gerenciador.usuario',),
        ),
        migrations.CreateModel(
            name='Presenca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricula', models.CharField(max_length=20, unique=True)),
                ('data', models.DateField(editable=False)),
                ('hora_entrada', models.TimeField(blank=True)),
                ('hora_saida', models.TimeField(blank=True)),
                ('status', models.CharField(blank=True, choices=[('P', 'Presente'), ('F', 'Faltou')], default=None, max_length=1)),
            ],
            options={
                'verbose_name': 'Presença',
                'unique_together': {('matricula', 'data')},
            },
        ),
    ]
