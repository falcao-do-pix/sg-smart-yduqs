#!/bin/sh

# Espera os bancos ficarem prontos
echo "Aguardando PostgreSQL..."
while ! nc -z db_postgres 5432; do
  sleep 1
done
echo "PostgreSQL Iniciado"

echo "Aguardando MySQL..."
while ! nc -z db_mysql 3306; do
  sleep 1
done
echo "MySQL Iniciado"

# Aplica migrações para cada banco de dados
echo "Aplicando migrações (default)..."
python manage.py migrate --database=default --noinput

echo "Aplicando migrações (presenca_postgres)..."
python manage.py migrate --database=presenca_postgres --noinput

# Cria o superusuário inicial (se não existir)
echo "Verificando/Criando superusuário inicial..."
python manage.py create_initial_superuser

# Coleta arquivos estáticos (descomente se for usar em produção com Gunicorn/Nginx)
# echo "Coletando arquivos estáticos..."
# python manage.py collectstatic --noinput --clear

# Executa o comando principal passado para o container
# (Ex: python manage.py runserver 0.0.0.0:8000 ou gunicorn)
echo "Iniciando aplicação Django..."
exec "$@"

