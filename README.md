# Aceleradev-python: Projeto final

## Status do build

![](https://github.com/johannesssf/aceleradev-final-project/workflows/ErrorsCenterCI/badge.svg)


## API Central de Erros (back-end)

A Central de Erros é um microsserviço que ajudara a centralizar e armazenar as mensagens geradas por diversos equipamentos. A centralização nos permite acessar de forma rápida todos os registros gerados, sem a necessidade de realizar consultas em diferentes equipamentos.


## Documentação da API REST (endpoints)

Neste endereço você pode conferir a documentação completa da API Rest.

[central-errors/api](https://johannesssf.github.io/aceleradev-final-project/docs/api.html)


## Tecnologias e dependências

* [Python](https://www.python.org/) 3.8.2
* [Django](https://www.djangoproject.com/) 2.2.13
* [djangorestframework](https://www.django-rest-framework.org/) 3.11.0
* [flake8](https://pypi.org/project/flake8/) 3.8.3
* [model-bakery](https://pypi.org/project/model-bakery/) 1.1.0
* [coverage](https://pypi.org/project/coverage/) 5.2
* [gunicorn](https://pypi.org/project/gunicorn/) 20.0.4
* [dj-database-url](https://pypi.org/project/dj-database-url/) 0.5.0
* [psycopg2](https://pypi.org/project/psycopg2/) 2.8.5
* [django-filter](https://pypi.org/project/django-filter/) 2.3.0
* [raml](https://raml.org/) 1.0
* [raml2html](https://github.com/raml2html/raml2html)

A instalação das dependências pode ser feita através do comando pip utilizando o arquivo *requirements.txt*.


## Acesso

A API encontra-se hospedado na plataforma [Heroku](https://www.heroku.com/) e a url para uso da API é: https://errorscenter.herokuapp.com/

Para interagir com a API, criar usuários e salvar os registros de erros, é preciso um usuário cadastrado e autenticado no sistema. Para o primeiro acesso utilizar o usuário: *admin* e a senha: *asdf1234* .

Para mais detalhes do uso da API ver a seção de documentação.
