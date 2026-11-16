# 🌱 Plantário

## 1. Sobre o projeto

O **Plantário** é uma API REST desenvolvida para registrar e acompanhar o crescimento de plantas.

O sistema permite cadastrar plantas, consultar informações, atualizar dados e excluir registros. Também permite registrar informações sobre o crescimento de cada planta, como data do registro, altura e descrição.

O objetivo é facilitar o acompanhamento do desenvolvimento das plantas por meio de uma aplicação organizada e com persistência de dados.

## 2. Tecnologias utilizadas

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn

## 3. Estrutura do banco de dados

O sistema utiliza SQLite para armazenar os dados.

Atualmente, possui dois modelos principais:

### Planta

Armazena as informações das plantas:

- `id`: identificador da planta;
- `nome`: nome da planta;
- `especie`: espécie da planta;
- `data_plantio`: data em que foi plantada;
- `local`: local onde a planta está.

### RegistroCrescimento

Armazena os registros de desenvolvimento de cada planta:

- `id_registro`: identificador do registro;
- `data_registro`: data em que o crescimento foi registrado;
- `altura`: altura registrada, quando informada;
- `descricao`: descrição do desenvolvimento;
- `planta_id`: identificador da planta relacionada.

Uma planta pode possuir vários registros de crescimento. O relacionamento é de um para muitos.

## 4. Funcionalidades da API

### Cadastro e gerenciamento de plantas

| Método | Rota | Descrição |
|---|---|---|
| POST | `/plantas` | Cadastrar uma planta |
| GET | `/plantas` | Listar plantas |
| GET | `/plantas/{planta_id}` | Consultar uma planta |
| PUT | `/plantas/{planta_id}` | Atualizar uma planta |
| DELETE | `/plantas/{planta_id}` | Excluir uma planta |

### Registros de crescimento

| Método | Rota | Descrição |
|---|---|---|
| POST | `/plantas/{planta_id}/registros` | Cadastrar um registro de crescimento |
| GET | `/plantas/{planta_id}/registros` | Listar os registros de uma planta |
| GET | `/plantas/{planta_id}/registros/{registro_id}` | Consultar um registro |
| PUT | `/plantas/{planta_id}/registros/{registro_id}` | Atualizar um registro |
| DELETE | `/plantas/{planta_id}/registros/{registro_id}` | Excluir um registro |

## 5. Validações e regras de negócio

O sistema possui validações para garantir a consistência das informações cadastradas.

Entre elas:

- Campos de texto obrigatórios não podem ficar vazios;
- A data de plantio não pode ser futura;
- A data do registro de crescimento não pode ser futura;
- A altura não pode ser negativa;
- A descrição do registro não pode ficar vazia;
- Não é permitido cadastrar um registro de crescimento com data anterior à data de plantio da planta.

Quando uma planta ou um registro não é encontrado, a API retorna uma resposta de erro HTTP 404.

As informações inválidas são rejeitadas pela API, com respostas apropriadas.

## 6. Busca, filtros, ordenação e paginação

A listagem de plantas permite:

- Busca geral por nome, espécie ou local;
- Filtro por espécie;
- Ordenação por identificador, nome, espécie, data de plantio ou local;
- Ordenação crescente ou decrescente;
- Paginação dos resultados;
- Definição do limite de plantas por página.

Os parâmetros disponíveis são:

| Parâmetro | Descrição |
|---|---|
| `Busca_Geral` | Busca por nome, espécie ou local |
| `Por_Especie` | Filtra pela espécie |
| `Ordenar_Por` | Define o campo de ordenação |
| `Ordem` | Define a ordem crescente ou decrescente |
| `Pagina_Consulta` | Define a página consultada |
| `Limite_de_plantas` | Define a quantidade de plantas por página |

## 7. Banco de dados e persistência

O projeto utiliza SQLite para armazenar os dados.

A conexão com o banco é realizada por meio do SQLAlchemy. Dessa forma, os registros permanecem armazenados mesmo após o encerramento e a reinicialização do servidor.

## 8. Como executar o projeto

### Pré-requisitos

- Python instalado;
- Git instalado.

### Instalação

Clone o repositório:

```bash
git clone https://github.com/angela1742/Plantario.git
```

Entre na pasta do projeto:

```bash
cd Plantario
```

Crie um ambiente virtual:

```bash
python3 -m venv .venv
```

Ative o ambiente virtual:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

Inicie o servidor:

```bash
uvicorn main:app --reload
```

## 9. Documentação da API

Após iniciar o servidor, a documentação interativa pode ser acessada pelo endereço:

```text
http://127.0.0.1:8000/docs
```

Nela é possível visualizar as rotas, consultar os parâmetros e testar as operações da API.

## 10. Estrutura dos arquivos

- `main.py`: implementação da API e suas rotas;
- `models.py`: modelos e relacionamentos do banco de dados;
- `schemas.py`: estruturas e validações dos dados;
- `database.py`: configuração da conexão com o banco de dados;
- `plantario.db`: banco de dados SQLite.

---

**Projeto acadêmico — Sistemas de Informação.**
