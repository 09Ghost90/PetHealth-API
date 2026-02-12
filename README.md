# 🐾 API REST — PetHealth API

##  Sistema

API REST para controle de vacinação de pets em uma clínica veterinária.

## Contexto Real

API totalmente testada com validação automática de regras de negócios e permissões.

Sistema baseado no fluxo real de uma clínica veterinária:

- **Tutores** levam seus pets para vacinação.
- **Funcionários** da clínica registram as vacinas aplicadas.
- **Tutores** podem visualizar apenas os seus próprios pets e histórico de vacinação.
- **Funcionários (admin)** possuem acesso total.

---

##  Regras de Negócio

###  Controle de Acesso

- Um tutor **só pode visualizar e manipular os seus próprios pets**.
- Um tutor **não pode acessar dados de pets de outros tutores**.
- **Funcionários** (`is_staff=True`) possuem acesso total.
- Usuário **não autenticado** não acessa nenhum recurso.

---

##  Modelagem do Sistema

### Relacionamentos

- Um **Tutor** pode possuir vários **Pets**.
- Um **Pet** pertence a um único **Tutor**.
- Um **Pet** pode receber várias **Vacinas**.
- Uma vacina pode ser aplicada em vários pets (registro independente).
- Apenas **funcionários registram vacinas**.
- Tutores apenas **visualizam**.

---

##  Estrutura do Projeto

```
core/        → Configuração principal do projeto
users/       → Usuários e Tutores
pets/        → Gerenciamento de pets
vaccines/    → Registro de vacinação
```

###  Motivação da Estrutura

A divisão em apps foi feita visando:

- **Organização**
- **Escalabilidade**
- **Facilidade de manutenção**
- **Separação clara de responsabilidades**
- **Boas práticas com Django**

---

##  Dependências

- **Django REST Framework (DRF)** → Construção da API
- **SimpleJWT** → Autenticação via JWT
- **python-dotenv** → Variáveis de ambiente
- **SQLite** → Banco de dados padrão Django

---

##  Autenticação — JWT (SimpleJWT)

A API utiliza autenticação JWT por ser:

- **Stateless**
- **Escalável**
- **Padrão em APIs REST modernas**

### Rotas de Autenticação

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/auth/register/` | Criar usuário |
| POST | `/api/auth/login/` | Gerar token |
| POST | `/api/auth/refresh/` | Renovar token |

Obs: Refresh pode ser alterado em core/settings.py

 **Observação:**

- Sempre usar `/` no final da rota.
- Não enviar dados como query parameters é uma questão de segurança.
- Enviar JSON no body.

---

##  Usuários e Perfis

**Nem todo usuário é necessariamente tutor.**

### User (Django)

Responsável por:

- `username`
-  email
- `password`
- autenticação
- permissões (`is_staff`)
- is_active

### Tutor

Perfil do cliente dono do pet:

```
Tutor
- id
- user (OneToOne)
- telefone
- endereco
```

### 🔍 Por que separar User e Tutor?

A separação entre `User` e `Tutor` foi feita para:

- Evitar duplicação de dados
- Permitir funcionários sem vínculo com pets
- Facilitar expansão futura (CPF, múltiplos endereços, histórico etc.)

---

##  Entidades Principais

### Pet

```
Pet
- id
- name
- especie
- raca
- data_nascimento
- tutor (ForeignKey)
```

### Regras aplicadas na View:

- `GET /api/pets/` → lista apenas pets do tutor
- `GET /api/pets/{id}/` → acessa apenas se for dono
- `POST /api/pets/` → pet já nasce vinculado ao tutor autenticado
- `PUT/PATCH` → não permite trocar tutor
- `DELETE` → só remove o próprio pet

---

##  Vacinas

### Modelo:

```
- id
- pet (ForeignKey)
- name
- applied_at
- next_dose
- notes
```

### Regras:

- Um pet pode ter várias vacinas.
- Tutor **não cria vacina**.
- **Funcionário (admin)** registra vacina.
- Tutor apenas **visualiza**.
- Tutor não vê vacina de pet que não é dele.

---

## Utilização Inicial da API

### 1️⃣ Criar Usuário

**POST** `/api/auth/register/`

```json
{
  "username": "tutor2",
  "email": "tutor2@email.com",
  "password": ".9B`zf86_T:&",
  "telefone": "31999999999",
  "endereco": "Rua B, 456"
}
```

### 2️⃣ Login

**POST** `/api/auth/login/`

```json
{
  "username": "tutor2",
  "password": ".9B`zf86_T:&"
}
```

**Retorna:**

```json
{
  "refresh": "...",
  "access": "..."
}
```

**Utilizar o token:**

```
Authorization: Bearer <access_token>
```

---

## 🔎 Endpoints Principais

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/pets/` | Lista pets do tutor |
| POST | `/api/pets/` | Criar pet |
| GET | `/api/pets/{id}/` | Detalhe do pet |
| GET | `/api/pets/{id}/vaccines/` | Listar vacinas do pet |
| POST | `/api/pets/{id}/vaccines/` | Registrar vacina (admin) |

---

##  Testes Automatizados

O projeto inclui testes automatizados para:

- Autenticação
- Controle de acesso
- Permissões de tutor
- Permissões de admin
- Associação correta entre tutor e pet
- Registro de vacinas

---

##  Docker (Execução Simplificada)

Para rodar o projeto:

```bash
docker compose up --build
```

Ou sem Docker:

```bash
python manage.py migrate
python manage.py runserver
```

---

##  Segurança por Padrão

- Todas as rotas protegidas por padrão.
- Permissões explícitas nas ViewSets.
- Tutor nunca é enviado no body.
- Associação automática via `request.user`.
- JWT com tempo de expiração configurado.

---

## Testes Automatizados

O projeto possui testes automatizados implementados utilizando o framework de testes nativo do Django em conjunto com o APITestCase do Django REST Framework.

Os testes garantem a integridades das principais regras de negócio e controle de permissão da API.

Ações dos testes:

### Autenticação

- Registro cria usuário e perfil Tutor automaticamente 
- Login retorna token JWT válidos

### Pets

- Tutor cria pet vinculado automaticamente a si
- Tutor só visualiza seus próprios pets
- Tutor não acessa pet de outro tutor
- Tutor não consegue alterar tutor do pet

### Vacinas

- Tutor não pode registrar vacina
- Funcionário (is_staff) pode registrar vacina
- Tutor visualiza apenas vacinas de seus pets

## Execução de testes

Rodar localmente:

```bash
python manage.py test
```

Rodar via Docker detalhadamente:

```bash
sudo docker compose run --rm api python manage.py test -v 2
```

---

## Documentação da API (Swagger / OpenAPI)

- Swagger UP: http://127.0.0.1:8000/api/docs/
- OpenAPI Schema (JSON): http://127.0.0.1:8000/api/schema/

## Coleção do Insomnia (testes manuais)

A coleção de requisições está disponível em:

- docs/insomnia_collection.json

Como importar:
1. Abra o Insomnia
2. Import -> From file
3. Selecione `docs/insomnia_collection.yaml`

---
