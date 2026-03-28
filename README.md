# Organização e Tarefas — Equipe Cliente

**Repositório:** `tftp-client-python`  
**Objetivo:** Construir um cliente TFTP isolado, aderente à RFC 1350, capaz de consumir servidores externos/comerciais, com divisão de trabalho alinhada aos diagramas C4.

---

## Diretriz Arquitetural

Este repositório representa o lado Cliente do sistema.

A organização segue os três níveis do modelo C4:

- **Nível 1 — Contexto:** define o sistema `TFTP Client Python` e suas entidades externas.
- **Nível 2 — Container:** representa a aplicação Python e suas dependências externas.
- **Nível 3 — Componentes:** detalha a divisão interna em módulos independentes.

Cada integrante é responsável por componentes específicos do Nível 3.

---

## Interpretação dos Diagramas C4

### Nível 1 — Contexto

Deve representar:

- Sistema principal: `TFTP Client Python`
- Ator principal: `Usuário`
- Sistema externo: `Servidor TFTP Externo/Comercial`
- Dependência externa: `Sistema de Arquivos Local`

Este nível descreve quem utiliza o cliente e com quais sistemas ele interage.

---

### Nível 2 — Container

Deve representar:

- Container principal: `Aplicação Python do Cliente`
- Dependências externas:
  - Rede UDP
  - Sistema de Arquivos Local

Como o sistema é simples, apenas um container é necessário.

Este nível descreve onde o cliente é executado e suas integrações externas.

---

### Nível 3 — Componentes

Deve conter os seguintes componentes:

- `CLI / Argument Parser`
- `Transfer Manager`
- `TFTP Packet API`
- `UDP Socket Adapter`
- `File Access`

Este nível descreve a organização interna da aplicação.

#### Relações esperadas

- `CLI / Argument Parser` → `Transfer Manager`
- `Transfer Manager` → `TFTP Packet API`
- `Transfer Manager` → `UDP Socket Adapter`
- `Transfer Manager` → `File Access`

#### Restrições

- `UDP Socket Adapter` não contém lógica de protocolo
- `File Access` não contém lógica de protocolo
- `TFTP Packet API` não acessa rede nem disco
- `CLI / Argument Parser` não manipula pacotes nem arquivos

---

## Papéis e Responsabilidades

### Arquiteto e Revisor - [Nome]

Responsável pela definição e manutenção da arquitetura do cliente.

#### Responsabilidades

- Elaborar os diagramas C4 (Níveis 1, 2 e 3)
- Criar a estrutura inicial do repositório
- Implementar:
  - `client.py`
  - `cli.py`
  - `transfer_manager.py`
- Criar `INTERFACE.md` e `README.md`
- Garantir aderência ao modelo C4

#### Revisão

- Aprovar Pull Requests relacionados aos componentes de borda
- Verificar:
  - aderência ao diagrama
  - separação de responsabilidades
  - ausência de acoplamento indevido

---

### Engenheiro de Redes e Testes - [Nome]

Responsável pelos componentes de borda e manipulação de dados.

#### Componentes

- `UDP Socket Adapter`
- `File Access`
- `TFTP Packet API`

#### Responsabilidades

- Implementar comunicação UDP
- Implementar leitura e escrita de arquivos
- Construir builders e parsers de pacotes TFTP
- Realizar testes com servidores externos
- Produzir evidências de interoperabilidade

---

## Regras de Arquitetura

### CLI / Argument Parser

Pode:
- utilizar `argparse`
- ler parâmetros de entrada
- iniciar o fluxo da aplicação

Não pode:
- acessar rede
- acessar disco
- manipular pacotes

---

### Transfer Manager

Pode:
- controlar o fluxo de `get` e `put`
- coordenar os demais componentes

Não pode:
- acessar diretamente socket
- acessar arquivos
- manipular bytes diretamente

---

### TFTP Packet API

Pode:
- montar e desmontar pacotes
- validar estrutura conforme RFC 1350

Não pode:
- acessar rede
- acessar disco
- controlar fluxo da aplicação

---

### UDP Socket Adapter

Pode:
- abrir e configurar socket
- enviar e receber dados
- controlar timeout

Não pode:
- interpretar protocolo
- acessar disco
- decidir fluxo

---

### File Access

Pode:
- ler arquivos para upload
- escrever arquivos recebidos
- validar caminhos

Não pode:
- interpretar pacotes
- acessar socket
- controlar fluxo

---

## Estrutura do Projeto

\`\`\`text
tftp-client-python/
├─ docs/
│  └─ c4/
│     ├─ nivel-1-contexto.drawio
│     ├─ nivel-2-container.drawio
│     └─ nivel-3-componentes.drawio
├─ INTERFACE.md
├─ README.md
├─ src/
│  └─ tftp_client/
│     ├─ __init__.py
│     ├─ client.py
│     ├─ cli.py
│     ├─ transfer_manager.py
│     ├─ packet_api.py
│     ├─ udp_adapter.py
│     ├─ file_access.py
│     └─ errors.py
└─ tests/
   ├─ unit/
   └─ integration/
\`\`\`
