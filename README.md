###para rodar: python3 manage.py runserver



##passo a passo usado para a criação desse projeto

1- criando ambiente virtual

python3 -m venv venv

source ./venv/bin/activate

pip install django djangorestframework django_cors_headers

pip freeze

pip freeze > requirements.txt

django-admin startproject api_root

python3 manage.py startapp api_rest

python3 manage.py runserver (testando pra ver se está rodando até aqui)

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py createsuperuser

python3 manage.py runserver

python3 manage.py (só pra ver os comandos que podem ser feitos com esse arquivo)# CHAT_API
