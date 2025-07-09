# 🏛️ Sistema de Leilão em Tempo Real com FastAPI + RabbitMQ

Este projeto simula uma casa de leilões em tempo real com participantes conectados via terminal. Cada item do leilão é publicado por um servidor FastAPI e todos os consumidores conectados recebem os itens e podem enviar seus lances.

O sistema utiliza RabbitMQ como um message broker para garantir a entrega de mensagens de forma assíncrona e em tempo real para todos os participantes.

## 📋 Requisitos

Para executar este projeto, você precisará ter os seguintes softwares instalados em sua máquina:

- Python 3.13 ou superior
- Docker e Docker Compose
- Poetry (para gerenciar as dependências do Python)

## ⚙️ Instalando o Poetry

Se você ainda não tem o Poetry instalado, execute o comando abaixo em seu terminal para instalá-lo:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

# Dependências do Projeto

Após instalar o Poetry, clone este repositório e, na pasta raiz do projeto, instale as dependências com o seguinte comando:

```bash
poetry install
```
# Executando a Aplicação

Para colocar o sistema de leilão no ar, é necessário iniciar três componentes, preferencialmente em terminais separados: o servidor de mensageria (RabbitMQ), o publicador de itens (FastAPI) e os clientes (consumidores).

## Passo 1: Iniciar o Servidor RabbitMQ

O RabbitMQ é o coração da nossa comunicação em tempo real. Para iniciá-lo em um container Docker, execute o seguinte comando na raiz do projeto:

```bash
docker-compose up -d
```

## Iniciar o Servidor FastAPI (Publicador)

O servidor FastAPI é responsável por publicar os itens que serão leiloados. Para iniciá-lo, execute o seguinte comando em um novo terminal:

```bash
fastapi dev leilao_pub/main.py
```

## Executar os Clientes (Consumidores)

Cada cliente que desejar participar do leilão deve executar o script `consumer.py`. Abra um novo terminal para cada cliente que você desejar conectar.

### Em Linux ou macOS:

```bash
python3 consumer.py
```

Cada terminal executando este script se tornará um participante ativo no leilão, podendo visualizar os itens e enviar lances em tempo real assim que eles forem publicados.

## 🏗️ Diagrama Simplificado da Arquitetura

```
+-------------------+      +------------------+      +-------------------+
|                   |      |                  |      |                   |
|  Cliente 1        +------>                  <------+  Servidor FastAPI   |
|  (consumer.py)    |      |                  |      |  (Leiloeiro)      |
|                   |      |                  |      |                   |
+-------------------+      |     RabbitMQ     |      +-------------------+

+-------------------+      |                  |
|                   |      |                  |
|  Cliente 2        +------>                  |
|  (consumer.py)    |      |                  |
|                   |      |                  |
+-------------------+      +------------------+
```
