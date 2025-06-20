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
* **Servidor de Produção:** Nginx, Gunicorn
* **Frontend (Templates):** HTML, Tailwind CSS
* **Gráficos:** Chart.js

## ⚙️ Pré-requisitos

Antes de começar, certifique-se de que você tem as seguintes ferramentas instaladas na sua máquina:

* [Git](https://git-scm.com/)
* [Docker](https://www.docker.com/products/docker-desktop/)
* [Docker Compose](https://docs.docker.com/compose/install/)

---

## 🚀 Ambiente de Desenvolvimento

Siga estes passos para configurar e rodar o projeto localmente para fins de desenvolvimento.

### 1. Clonar o Repositório

```bash
git clone [https://github.com/falcao-do-pix/sg-smart-yduqs.git](https://github.com/falcao-do-pix/sg-smart-yduqs.git)
cd sg-smart-yduqs
```

### 2. Configurar Variáveis de Ambiente

O projeto utiliza um arquivo `.env` para as configurações.

**a.** Crie o arquivo `.env` na raiz do projeto. É recomendado copiar do exemplo (se existir) ou criar um novo.
```bash
# Se houver um .env.example no projeto:
cp .env.example .env

# Ou crie um novo:
touch .env
```

**b.** Preencha o `.env` com as configurações para o ambiente de desenvolvimento.

### 3. Construir e Iniciar os Containers

Com o Docker rodando e o `.env` configurado, execute:

```bash
sudo docker compose -f docker-compose.yml up --build
```
* `--build`: Força a reconstrução da imagem. Essencial na primeira vez.
* Use `docker-compose.yml` para o ambiente de desenvolvimento.

### 4. Acessar a Aplicação

* **Portal do Aluno:** `http://localhost:8000/alunos/login/`
* **Dashboard:** `http://localhost:8000/dashboard/login/`
* **Django Admin:** `http://localhost:8000/admin/`

---

## ☁️ Ambiente de Produção

Siga estes passos para implantar a aplicação em um servidor de produção (VPS na nuvem).

### 1. Configurar o Servidor

* Acesse seu servidor na nuvem (ex: Google Cloud, AWS).
* Clone o repositório como no passo de desenvolvimento.
* Certifique-se de que as portas **80 (HTTP)** e **443 (HTTPS)** estão abertas no firewall do seu provedor de nuvem.

### 2. Configurar Variáveis de Ambiente para Produção

**a.** Na raiz do projeto no servidor, crie o arquivo `.env.prod`. **Este arquivo nunca deve ser enviado para o Git.**


### 3. Construir e Iniciar os Containers de Produção

Use o arquivo `docker-compose.prod.yml` e passe o arquivo de ambiente explicitamente.

```bash
sudo docker compose --env-file .env.prod -f docker-compose.prod.yml up --build -d
```
* `-f docker-compose.prod.yml`: Especifica o arquivo de compose de produção.
* `--env-file .env.prod`: Garante que as variáveis de produção sejam carregadas.
* `-d`: Roda os containers em segundo plano (detached mode).

### 4. Configurar HTTPS com Certbot

Após iniciar os containers, siga o guia `httpsg_guide_final` para obter e instalar o certificado SSL/TLS.

### 5. Acessar a Aplicação em Produção

Após configurar o HTTPS, sua aplicação estará disponível de forma segura em: `https://seu_dominio.com`

## 💻 Comandos Úteis do Docker

### Executar Comandos `manage.py`

```bash
# No ambiente de produção
sudo docker compose -f docker-compose.prod.yml exec django_app python manage.py <comando>

# Exemplo: Abrir o shell
sudo docker compose -f docker-compose.prod.yml exec django_app python manage.py shell
```

### Visualizar Logs

```bash
# Ver logs de um serviço específico em tempo real
sudo docker compose -f docker-compose.prod.yml logs -f <nome_do_servico>

# Exemplo: Ver logs do Nginx
sudo docker compose -f docker-compose.prod.yml logs -f nginx
```

### Parar a Aplicação

```bash
# Para parar e remover os containers de produção
sudo docker compose -f docker-compose.prod.yml down
```
*(Os dados salvos nos volumes dos bancos de dados persistirão).*
