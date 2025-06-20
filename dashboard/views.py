from django.shortcuts import render, redirect
from gerenciador.models import Aluno, Presenca
from django.db.models import Count, Q
from datetime import datetime, timedelta, time
from django.contrib import messages
from collections import defaultdict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncDate
from .decorators import staff_required
import json
import calendar

def login_view_dashboard(request): # O nome da view pode ser diferente
    if request.user.is_authenticated:
        return redirect('dashboard') # Redireciona se já estiver logado
    if request.method == 'POST':
        # ... sua lógica de autenticação para o dashboard ...
        # Exemplo:
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        user = authenticate(request, username=username_input, password=password_input)
        if user is not None:
            # Verifique se o usuário tem permissão para acessar o dashboard
            if user.is_staff: # Exemplo de verificação
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Você não tem permissão para acessar o dashboard.")
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    return render(request, 'dashboard/login.html') # Seu template de login do dashboard

def logout_view_dashboard(request): # Nome da view pode ser diferente
    logout(request)
    messages.info(request, "Você saiu com sucesso.")
    return redirect('login_dashboard') # Redireciona para a página de login do dashboard

@staff_required
def dashboard_view(request):
    # Filtros da URL
    curso = request.GET.get("curso", None)
    periodo = request.GET.get("periodo", '7d')

    if periodo == '7d':
        data_inicio = datetime.now() - timedelta(days=7)
    elif periodo == '30d':
        data_inicio = datetime.now() - timedelta(days=30)
    elif periodo == '90d':
        data_inicio = datetime.now() - timedelta(days=90)
    else:
        data_inicio = datetime.now() - timedelta(days=7)

    presenca = Presenca.objects.filter(data__gte=data_inicio)
    if curso:
        presenca = presenca.value('matricula__curso')

    total_alunos = Aluno.objects.count()
    media_atrasados = presenca.filter(status='').count() / max(total_alunos, 1)
    alunos_por_curso = Aluno.objects.values('curso').annotate(total=Count('curso'))
    alunos_pontuais = presenca.filter(status='P').count()
    alunos_atrasados = presenca.filter(status='').count()

    # Evolução diária por status
    evolucao_por_status_raw = presenca.values('data', 'status').annotate(total=Count('id')).order_by('data')
    evolucao_por_status = defaultdict(lambda: {'P': 0, 'A': 0, 'F': 0})
    for item in evolucao_por_status_raw:
        data_str = item['data'].strftime('%Y-%m-%d')
        evolucao_por_status[data_str][item['status']] = item['total']

    # Obtém presenças filtradas por status e período
    presencas_filtradas = presenca.filter(status__in=['P', 'A'])

    # Mapeia matrícula -> curso (vindo do model Aluno)
    alunos = Aluno.objects.all()
    matricula_para_curso = {aluno.matricula: aluno.curso for aluno in alunos}

    # Contador de presenças por curso
    presencas_por_curso = defaultdict(int)
    total_presencas = 0

    for p in presencas_filtradas:
        curso = matricula_para_curso.get(p.matricula)
        if curso:
            presencas_por_curso[curso] += 1
            total_presencas += 1

    # Transforma em estrutura para o gráfico de percentual
    percentual_por_curso = [
        {
            'curso': curso,
            'percentual': round((total / total_presencas) * 100, 2)
        }
        for curso, total in presencas_por_curso.items()
    ]

    context = {
        'total_alunos': total_alunos,
        'media_atrasados': round(media_atrasados, 2),
        'alunos_por_curso': list(alunos_por_curso),
        'alunos_pontuais': alunos_pontuais,
        'alunos_atrasados': alunos_atrasados,
        'evolucao_por_status': dict(evolucao_por_status),
        'percentual_por_curso': percentual_por_curso,
        'percentual_por_curso': percentual_por_curso,
    }

    # Distribuição de horários de entrada (arredondando por hora)
    entradas = (
        presenca.exclude(hora_entrada=None)
        .values_list('hora_entrada', flat=True)
    )

    # Arredondar hora para faixa (por hora: 07h, 08h, etc.)
    faixas_horarias = defaultdict(int)
    for h in entradas:
        hora = h.replace(minute=0, second=0, microsecond=0)
        faixas_horarias[hora.strftime('%H:%M')] += 1

    labels_horarios = sorted(faixas_horarias.keys())
    valores_horarios = [faixas_horarias[label] for label in labels_horarios]

    context.update({
        'labels_horarios': json.dumps(labels_horarios),
        'valores_horarios': valores_horarios,
    })

    # Agrupamento por dia da semana
    dias_semana = (
        presenca.values_list('data', flat=True)
    )

    contagem_dias = defaultdict(int)
    for data in dias_semana:
        nome_dia = calendar.day_name[data.weekday()]  # 'Monday', 'Tuesday', etc.
        contagem_dias[nome_dia] += 1

    # Ordena de segunda a domingo
    ordem_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    labels_dias_semana = [calendar.day_name[i] for i in range(7)]
    valores_dias_semana = [contagem_dias.get(dia, 0) for dia in ordem_dias]

    context.update({
        'labels_dias_semana': json.dumps(labels_dias_semana),
        'valores_dias_semana': valores_dias_semana,
    })

    # Agrupamento por dia: total e presentes
    presencas_por_data = (
        presenca
        .values('data')
        .annotate(
            total=Count('id'),
            presentes=Count('id', filter=Q(status='P'))
        )
        .order_by('data')
    )

    datas_taxa = [p['data'].strftime('%Y-%m-%d') for p in presencas_por_data]
    taxas = [
        round((p['presentes'] / p['total']) * 100, 2) if p['total'] > 0 else 0
        for p in presencas_por_data
    ]

    context.update({
        'taxa_datas': json.dumps(datas_taxa),
        'taxa_valores': taxas,
    })

    return render(request, 'dashboard/dashboard.html', context)
