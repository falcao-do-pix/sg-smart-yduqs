import time
import logging
import requests
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError, ProgrammingError

logger = logging.getLogger(__name__)

# Configurações
API_BASE = "http://localhost:8000/api/"
BOT_CREDENCIAIS = {
    'email': 'portal_bot@interno.com',
    'password': 'P@ssw0rd!23',
    'username': 'portal_bot',
    'matricula': '11111111',
}

# Tokens
INTERNAL_JWT_ACCESS = None
INTERNAL_JWT_REFRESH = None
INTERNAL_JWT_EXPIRATION = 0  # epoch

def criar_superusuario_local():
    """Cria o superusuário 'portal_bot' via ORM, se possível."""
    try:
        User = get_user_model()
        if not User.objects.filter(email=BOT_CREDENCIAIS['email']).exists():
            logger.info("Criando superusuário portal_bot...")
            User.objects.create_superuser(
                email=BOT_CREDENCIAIS['email'],
                password=BOT_CREDENCIAIS['password'],
                matricula=BOT_CREDENCIAIS['matricula']
            )
            logger.info("Superusuário criado com sucesso.")
        else:
            logger.info("Superusuário já existe.")
    except (OperationalError, ProgrammingError) as e:
        # Isso acontece quando as tabelas ainda não existem (ex: makemigrations/migrate)
        logger.warning(f"Não foi possível verificar/criar o superusuário (banco não pronto): {e}")

def login_bot():
    """Faz login com o bot e salva os tokens JWT."""
    global INTERNAL_JWT_ACCESS, INTERNAL_JWT_REFRESH, INTERNAL_JWT_EXPIRATION

    try:
        response = requests.post(f"{API_BASE}token/", json={
            'matricula': BOT_CREDENCIAIS['matricula'],
            'password': BOT_CREDENCIAIS['password']
        })
        # print(response.text)
        if response.status_code == 200:
            data = response.json()
            INTERNAL_JWT_ACCESS = data['access']
            INTERNAL_JWT_REFRESH = data['refresh']
            INTERNAL_JWT_EXPIRATION = time.time() + 60 * 4  # 4 minutos
            logger.info("Login do bot realizado.")
        else:
            logger.error("Erro no login do bot(teste): %s", response.response)
    except Exception as e:
        logger.error("Erro de rede no login do bot: %s", str(e))

def refresh_token_bot():
    """Renova o token de acesso usando o refresh token."""
    global INTERNAL_JWT_ACCESS, INTERNAL_JWT_EXPIRATION
    try:
        response = requests.post(f"{API_BASE}token/refresh/", json={
            'refresh': INTERNAL_JWT_REFRESH
        })
        if response.status_code == 200:
            INTERNAL_JWT_ACCESS = response.json()['access']
            INTERNAL_JWT_EXPIRATION = time.time() + 60 * 4
            logger.info("Token renovado com sucesso.")
        else:
            logger.warning("Falha ao renovar token. Reautenticando...")
            login_bot()
    except Exception as e:
        logger.error("Erro ao renovar token: %s", str(e))
        login_bot()

def get_internal_auth_headers():
    """Retorna headers de autenticação interna válidos."""
    if INTERNAL_JWT_ACCESS is None or time.time() >= INTERNAL_JWT_EXPIRATION:
        if INTERNAL_JWT_REFRESH:
            refresh_token_bot()
        else:
            login_bot()
    return {'Authorization': f'Bearer {INTERNAL_JWT_ACCESS}'}

def inicializar_bot():
    """Inicializa o bot manualmente após as migrações."""
    criar_superusuario_local()
    login_bot()
