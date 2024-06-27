My drive

Objetivo
O objetivo deste projeto é desenvolver uma aplicação web completa utilizando Django e JavaScript, que permite a gestão de arquivos e pastas. A aplicação oferece funcionalidades de autenticação e autorização de usuários, organização de arquivos, e uma interface gráfica intuitiva.

Organização do Projeto
O projeto está organizado nas seguintes pastas e arquivos:

core/: Aplicação principal com funcionalidades de gestão de Autenticação.

models.py: Modelos do Django para Users.
views.py: Visualizações para a gestão de Log in Sign up.
forms.py: Formulários de Autenticação.
templates/: Templates HTML para a interface do usuário.


foldermaster/: Aplicação principal com funcionalidades de gestão de arquivos e pastas.

models.py: Modelos do Django para pastas e arquivos.
views.py: Visualizações para a gestão de arquivos e pastas.
forms.py: Formulários utilizados na aplicação.
templates/: Templates HTML para a interface do usuário.


mydrive/: Configurações do projeto Django.

settings.py: Configurações gerais do projeto.
urls.py: URLs principais do projeto.
wsgi.py: Configuração WSGI para o projeto.

Requisitos do Projeto

Registo de Utilizadores usando Django
Login, Logout e Reset de Password
Criação de pastas, com a possibilidade de criar pastas dentro de pastas
Upload e download de ficheiros
Navegação entre pastas
Quota de 50MB por utilizador
Diferentes tipos de utilizadores (Staff e User)

Processo de Instalação
Pré-requisitos
Docker
Docker Compose
Make


Passos de Instalação
Clone o repositório do projeto.
Execute os seguintes comandos para configurar e iniciar o projeto:
make build
make migrate
make createsuperuser
make up


Docker Compose
O arquivo docker-compose.yml define os serviços necessários para a aplicação.

Licença
Este projeto está licenciado sob os termos da licença MIT.
