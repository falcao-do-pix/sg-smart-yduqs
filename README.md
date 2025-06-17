# SG Smart YDUQS - Sistema de Gestão Acadêmica

Este é o repositório do projeto SG Smart YDUQS, um sistema de gestão acadêmica desenvolvido em Django e conteinerizado com Docker. O sistema é dividido em três aplicações principais: um painel de gerenciamento de dados, um portal do aluno e um dashboard de análise de presença.

## ✨ Funcionalidades

* **Gerenciador (`gerenciador`):**
    * Serve como o núcleo do sistema e a API REST.
    * Gerencia os dados de alunos, professores e cursos.
    * Controla a autenticação e permissões.
* **Portal do Aluno (`portal_aluno`):**
    * Interface para os alunos se cadastrarem, fazerem login e consultarem suas informações.
    * Permite a edição de perfil e visualização de dados acadêmicos.
* **Dashboard (`dashboard`):**
    * Painel de análise visual para administradores.
    * Exibe estatísticas e gráficos sobre a presença e o fluxo de alunos na instituição.

## 🛠️ Tecnologias Utilizadas

* **Backend:** Django
* **Bancos de Dados:** PostgreSQL e MySQL
* **API:** Django REST Framework, Simple JWT
* **Conteinerização:** Docker, Docker Compose
* **Frontend (Templates):** HTML, Tailwind CSS
* **Gráficos:** Chart.js

## ⚙️ Pré-requisitos

Antes de começar, certifique-se de que você tem as seguintes ferramentas instaladas na sua máquina:

* [Git](https://git-scm.com/)
* [Docker](https://www.docker.com/products/docker-desktop/)
* [Docker Compose](https://docs.docker.com/compose/install/) (geralmente incluído com o Docker Desktop)

## 🚀 Instalação e Execução

Siga estes passos para configurar e rodar o ambiente de desenvolvimento localmente usando Docker.

### 1. Clonar o Repositório

Abra seu terminal e clone o projeto do GitHub:
```bash
git clone [https://github.com/falcao-do-pix/sg-smart-yduqs.git](https://github.com/falcao-do-pix/sg-smart-yduqs.git)
cd sg-smart-yduqs
```

### 2. Configurar Variáveis de Ambiente

O projeto utiliza um arquivo `.env` para gerenciar configurações sensíveis e específicas do ambiente.

**a.** Crie o arquivo `.env` na raiz do projeto. Você pode copiar o `.env.example` se ele existir, ou criar um novo.
```bash
cp .env.example .env
```
*(Nota: Se o arquivo `.env.example` não existir no repositório, crie um arquivo `.env` manualmente).*

### 3. Construir e Iniciar os Containers

Com o Docker rodando e o arquivo `.env` configurado, execute o seguinte comando na raiz do projeto:

```bash
sudo docker compose up --build
```

* `--build`: Força a reconstrução da imagem do aplicativo. É essencial na primeira vez ou após alterar o `Dockerfile` ou `requirements.txt`.
* O Docker irá construir a imagem do Django, baixar as imagens do PostgreSQL e MySQL, e iniciar todos os serviços.
* O script `entrypoint.sh` será executado, aplicando as migrações e criando o superusuário.

### 4. Acessar a Aplicação

Após os logs indicarem que o servidor Django iniciou, você pode acessar os diferentes portais:

* **Portal do Aluno (Login):** <http://localhost:8000/alunos/login/>
* **Dashboard (Login):** <http://localhost:8000/dashboard/login/>
* **Django Admin:** <http://localhost:8000/admin/>
    * **Usuário:** `admin` (ou o que você definiu em `DJANGO_SUPERUSER_USERNAME`)
    * **Senha:** `adminpass` (ou o que você definiu em `DJANGO_SUPERUSER_PASSWORD`)

## 💻 Desenvolvimento

### Executar Comandos `manage.py`

Para executar comandos como `makemigrations` ou `shell`, abra um **novo terminal**, navegue até a pasta do projeto e use `docker compose exec`:

```bash
# Criar novas migrações
sudo docker compose exec django_app python manage.py makemigrations

# Abrir o shell do Django
sudo docker compose exec django_app python manage.py shell
```

### Visualizar Logs

Você pode ver os logs em tempo real de cada serviço:

```bash
# Logs do aplicativo Django
sudo docker compose logs -f django_app

# Logs do PostgreSQL
sudo docker compose logs -f db_postgres

# Logs do MySQL
sudo docker compose logs -f db_mysql
```

### Parar a Aplicação

Para parar todos os containers, pressione `Ctrl+C` no terminal onde o `docker compose up` está rodando. Para parar e remover os containers, execute:

```bash
sudo docker compose down
```

*(Os dados dos bancos de dados salvos nos volumes persistirão).*
