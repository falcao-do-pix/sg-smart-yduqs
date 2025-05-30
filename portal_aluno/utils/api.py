from .middleware import get_internal_auth_headers
import requests

API_BASE = "http://localhost:8000/api/"  # ajuste conforme o ambiente

def listar_cursos():
    headers = get_internal_auth_headers()
    response = requests.get(f"{API_BASE}cursos/", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao obter cursos: {response.status_code}")
        return []

def buscar_cursos_por_nome(q):
    headers = get_internal_auth_headers()
    response = requests.get(f"{API_BASE}cursos/", headers=headers, params={"search": q})
    return response.json() if response.status_code == 200 else []

def criar_aluno(data):
    headers = get_internal_auth_headers()
    response = requests.post(f"{API_BASE}alunos/", headers=headers, json=data)
    return response

def obter_aluno_por_matricula(matricula):
    headers = get_internal_auth_headers()
    response = requests.get(f"{API_BASE}alunos/{matricula}/", headers=headers)
    return response.json() if response.status_code == 200 else None

def atualizar_aluno(matricula, data):
    headers = get_internal_auth_headers()
    response = requests.patch(f"{API_BASE}alunos/{matricula}/", headers=headers, json=data)
    return response

def get_user_auth_headers(token):
    """Cria os headers de autenticação Bearer com o token JWT do usuário."""
    return {"Authorization": f"Bearer {token}"}

def atualizar_perfil_aluno_api_com_matricula(token, matricula_aluno, data_to_update):
    """
    Atualiza os dados do perfil do aluno logado usando o endpoint /api/alunos/{matricula}/ via PATCH.
    """
    headers = get_user_auth_headers(token)
    update_url = f"{API_BASE}alunos/{matricula_aluno}/" # Constrói a URL com a matrícula

    try:
        # Envia a requisição PATCH com o token e os dados
        response = requests.patch(update_url, headers=headers, json=data_to_update)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao atualizar perfil: {e}")
        # Retorna um objeto de resposta simulado em caso de erro de conexão
        class MockResponse:
            status_code = 503
            def json(self): return {"detail": f"Erro de conexão: {e}"}
            def text(self): return f"Erro de conexão: {e}"
        return MockResponse()

def obter_dados_aluno_logado(token):
    """Busca os dados do aluno logado usando o endpoint /api/aluno/me/."""
    headers = get_user_auth_headers(token)
    try:
        # Garanta que a URL está correta. Se a view 'aluno_me' estiver
        # registrada como 'alunos/me/' na API, ajuste aqui.
        # Vamos assumir 'aluno/me/' por enquanto.
        response = requests.get(f"{API_BASE}aluno/me/", headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print("Erro 401: Token inválido ou expirado ao buscar /api/aluno/me/")
            return None
        else:
            print(f"Erro {response.status_code} ao buscar /api/aluno/me/: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao buscar /api/aluno/me/: {e}")
        return None