from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_GET
from .utils.api import criar_aluno, obter_aluno_por_matricula, atualizar_aluno, listar_cursos, buscar_cursos_por_nome, obter_dados_aluno_logado, atualizar_perfil_aluno_api_com_matricula
from .forms import AlunoRegisterForm
from django.http import JsonResponse
from gerenciador.models import Aluno
from django.contrib import messages
# from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from django.conf import settings
import requests


@login_required
def painel_aluno(request):
    """
    Exibe o painel do aluno, buscando os dados da API /api/aluno/me/.
    """
    access_token = request.session.get("access_token")

    if not access_token:
        messages.error(request, "Sessão inválida ou expirada. Faça login novamente.")
        return redirect('login_aluno')

    # Busca os dados do aluno na API
    aluno_data = obter_dados_aluno_logado(access_token)

    if not aluno_data:
        messages.error(request, "Sua sessão expirou ou não foi possível carregar seus dados. Por favor, faça login novamente.")
        # --- ADICIONADO LOGOUT AQUI PARA QUEBRAR O LOOP ---
        logout(request) # Limpa a sessão Django
        if 'access_token' in request.session: # Opcional: limpar explicitamente
            del request.session['access_token']
        if 'refresh_token' in request.session: # Opcional: limpar explicitamente
            del request.session['refresh_token']
        # --- FIM DA ADIÇÃO ---
        return redirect('login_aluno')

    # Passa os dados do aluno como contexto para o template
    context = {
        'aluno': aluno_data
    }
    return render(request, 'portal_aluno/painel.html', context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('painel_aluno')

    if request.method == 'POST':
        form = AlunoRegisterForm(request.POST)
        if form.is_valid():
            request.session['novo_aluno'] = {
                'nome': form.cleaned_data['nome'],
                'email': form.cleaned_data['email'],
                'matricula': form.cleaned_data['matricula'],
                'senha': form.cleaned_data['senha']
            }
            return redirect('selecionar_curso')
        else:
            # Se o formulário não for válido, renderiza a página com os erros
             return render(request, 'portal_aluno/register.html', {'form': form})
    else:
        form = AlunoRegisterForm()
    return render(request, 'portal_aluno/register.html', {'form': form})


# @login_required(login_url='login_aluno')  # ou remova se não exigir login aqui
def selecionar_curso_view(request):
    if request.user.is_authenticated:
        return redirect('painel_aluno')

    cursos = listar_cursos()  # API que retorna lista de cursos

    if request.method == "POST":
        curso_selecionado = request.POST.get("curso")

        if not curso_selecionado or curso_selecionado == '':
            messages.error(request, "Por favor, selecione um curso válido.")
            return render(request, 'portal_aluno/selecionar_curso.html', {
                'cursos': cursos,
                'curso_selecionado': curso_selecionado  # Para manter seleção se houver erro
            })

        dados_parciais = request.session.get("novo_aluno")
        if not dados_parciais:
            messages.error(request, "Sessão expirada. Por favor, preencha os dados novamente.")
            return redirect('cadastro_aluno')

        if curso_selecionado:
            dados_parciais['curso'] = curso_selecionado
            response = criar_aluno(dados_parciais)

            if response.status_code == 201:
                if 'novo_aluno' in request.session: # Garante que só deleta se existir
                    del request.session['novo_aluno']
                messages.success(request, "Cadastro realizado com sucesso. Faça login.")
                return redirect('login_aluno')
            else:
                try:
                    erro = response.json()
                except ValueError:  # JSONDecodeError é um subtipo
                    erro = response.text  # texto da resposta, pode ser HTML ou vazio
                    print(request, f"Erro ao cadastrar: {erro}")
                    messages.error(request, f"Erro ao cadastrar: {erro}")


    return render(request, 'portal_aluno/selecionar_curso.html', {'cursos': cursos})

@login_required
def editar_perfil_view(request):
    # 1. Pega o token da sessão
    access_token = request.session.get("access_token")
    if not access_token:
        messages.error(request, "Sessão inválida. Faça login para editar seu perfil.")
        logout(request)
        return redirect('login_aluno')

    # 2. Busca os dados atuais via API (para GET e para comparar no POST)
    aluno_atual = obter_dados_aluno_logado(access_token)
    if not aluno_atual:
        messages.error(request, "Não foi possível carregar seus dados atuais. Tente novamente.")
        logout(request)
        return redirect('login_aluno')

    if request.method == 'POST':
        # 3. Processa o formulário submetido
        data_to_update = {}
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip()
        nova_senha = request.POST.get('nova_senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # 4. Compara e adiciona apenas o que mudou
        if nome and nome != aluno_atual.get('nome'):
            data_to_update['nome'] = nome
        if email and email != aluno_atual.get('email'):
            data_to_update['email'] = email

        # 5. Valida e adiciona a nova senha (se houver)
        if nova_senha:
            if nova_senha != confirmar_senha:
                messages.error(request, "As senhas não coincidem.")
                return render(request, 'portal_aluno/editar_perfil.html', {'aluno': aluno_atual})
            try:
                validate_password(nova_senha, user=request.user)
                data_to_update['senha'] = nova_senha
            except ValidationError as e:
                messages.error(request, f"Erro na nova senha: {' '.join(list(e))}")
                return render(request, 'portal_aluno/editar_perfil.html', {'aluno': aluno_atual})

        # 6. Verifica se há algo para atualizar
        if not data_to_update:
            messages.info(request, "Nenhuma alteração foi fornecida.")
            return render(request, 'portal_aluno/editar_perfil.html', {'aluno': aluno_atual})

        # 7. Chama a nova função da API para atualizar
        matricula_do_aluno_logado = aluno_atual.get('matricula')
        response = atualizar_perfil_aluno_api_com_matricula(access_token, matricula_do_aluno_logado, data_to_update)

        # 8. Trata a resposta da API
        if response and response.status_code in [200, 204]:
            messages.success(request, "Perfil atualizado com sucesso!")
            if 'senha' in data_to_update: # Se mudou senha, força novo login
                messages.info(request, "Sua senha foi alterada. Por favor, faça login novamente com a nova senha.")
                logout(request)
                return redirect('login_aluno')
            return redirect('painel_aluno')
        else:
            # Tenta mostrar erros mais detalhados da API
            error_message = "Erro ao atualizar perfil."
            # ... (Lógica para extrair erro da API) ...
            messages.error(request, error_message)
            return render(request, 'portal_aluno/editar_perfil.html', {'aluno': aluno_atual})

    # 9. Se for GET, renderiza o template com os dados atuais
    return render(request, 'portal_aluno/editar_perfil.html', {'aluno': aluno_atual})

@require_GET
def buscar_cursos(request):
    query = request.GET.get('q', '')
    cursos = buscar_cursos_por_nome(query)
    return JsonResponse(cursos, safe=False)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('painel_aluno')

    if request.method == "POST":
        matricula_input = request.POST.get("matricula") # Renomeado para evitar conflito
        senha = request.POST.get("senha")

        payload = {
            "matricula": matricula_input,  # <--- CORRIGIDO AQUI!
            "password": senha
        }

        try:
            # Supondo que o endpoint esteja no app gerenciador
            # Verifique se settings.GERENCIADOR_API_URL está correto
            api_url = settings.GERENCIADOR_API_URL + "/api/token/"
            response = requests.post(api_url, json=payload)

            if response.status_code == 200:
                data = response.json()
                # Armazena os tokens na sessão
                request.session["access_token"] = data["access"]
                request.session["refresh_token"] = data["refresh"]

                # É crucial logar o usuário no sistema de autenticação do Django
                # para que @login_required funcione nas outras views do portal_aluno.
                # Como estamos usando Simple JWT, a autenticação "real" é via token.
                # Mas para as views do portal_aluno, precisamos de uma sessão Django.
                # Uma forma é usar o authenticate com o backend customizado (se ele retornar o usuário).
                user = authenticate(request, matricula=matricula_input, password=senha)
                if user is not None:
                    login(request, user) # Cria a sessão Django
                    return redirect("painel_aluno")
                else:
                    # Se authenticate falhou mesmo com token OK (estranho), avise.
                    messages.error(request, "Erro ao iniciar sessão local. Tente novamente.")

            else:
                messages.error(request, "Matrícula ou senha inválida.")
                try:
                    error_detail = response.json()
                    print(f"Erro da API de token: {error_detail}")
                except ValueError:
                    print(f"Erro da API de token (não JSON): {response.text}")

        except requests.exceptions.RequestException:
            messages.error(request, "Erro ao conectar com o servidor. Tente novamente.")

    return render(request, "portal_aluno/login.html")


@login_required
def logout_view(request):
    # Aqui você pode apenas redirecionar. O frontend limpa o token.
    return redirect('login_aluno')