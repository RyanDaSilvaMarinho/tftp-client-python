# tftp-client-python

## Objetivo 
Implementar um cliente TFTP em Python, aderente à RFC 1350, com separação de responsabilidades baseada no modelo C4 e interface de linha de comando

---

## Equipe:
* Fernando Luiz
* Ryan da Silva Marinho
* Wanderberg
* Gabriel Pepes Moda
* Gustavo Almada

## Diagramas C4

### Nível 1 — Contexto
![C4 Nível 1](<img width="894" height="721" alt="image" src="https://github.com/user-attachments/assets/c7b7aa05-3df8-440e-a4ff-e4386fcc56a3" />)

### Nível 2 — Container
![C4 Nível 2](<img width="631" height="811" alt="image" src="https://github.com/user-attachments/assets/b62205f1-2768-48c2-a380-be0707d1485e" />)

### Nível 3 — Componentes
![C4 Nível 3](<img width="859" height="1081" alt="image" src="https://github.com/user-attachments/assets/c29b72cd-7835-423e-abbb-c9b9f34ad411" />)

---

## Estrutura do Projeto
```
tftp-client-python/
├─ docs/c4/                  # Diagramas C4 (Níveis 1, 2 e 3)
├─ src/tftp_client/
│  ├─ client.py              # Ponto de entrada
│  ├─ cli.py                 # CLI / Argument Parser
│  ├─ transfer_manager.py    # Transfer Manager
│  ├─ packet_api.py          # TFTP Packet API
│  ├─ udp_adapter.py         # UDP Socket Adapter
│  ├─ file_access.py         # File Access
│  └─ errors.py              # Exceções do domínio
├─ tests/
│  ├─ unit/                  # Testes unitários (sem rede)
│  └─ integration/           # Testes com servidor TFTP real
├─ INTERFACE.md
└─ README.md
```

---

## Arquitetura — Separação de Responsabilidades

| Componente | Acessa Rede | Acessa Disco | Manipula Pacotes | Controla Fluxo |
|---|---|---|---|---|
| CLI / Arg Parser | ✗ | ✗ | ✗ | inicia |
| Transfer Manager | ✗ (delega) | ✗ (delega) | ✗ (delega) | ✔ |
| TFTP Packet API | ✗ | ✗ | ✔ | ✗ |
| UDP Socket Adapter | ✔ | ✗ | ✗ | ✗ |
| File Access | ✗ | ✔ | ✗ | ✗ |

---

## Como usar

### Pré-requisitos
- Python 3.10+

### Executando o cliente
```bash
# Baixar um arquivo do servidor
python -m tftp_client.client get <HOST> <PORTA> <ARQUIVO_REMOTO>

# Enviar um arquivo para o servidor
python -m tftp_client.client put <HOST> <PORTA> <ARQUIVO_LOCAL>

# Exemplos
python -m tftp_client.client get 127.0.0.1 69 teste.txt
python -m tftp_client.client put 127.0.0.1 69 envio.txt

# Com caminho local diferente
python -m tftp_client.client get 192.168.0.1 69 remoto.txt --local local.txt

# Com timeout customizado
python -m tftp_client.client get 192.168.0.1 69 arquivo.txt --timeout 10.0
```

---

## Testes

### Testes unitários (sem necessidade de servidor)
```bash
# Todos de uma vez
python -m unittest discover -s tests/unit -v

# Ou individualmente
python -m unittest tests/unit/test_packet_apy.py -v
python -m unittest tests/unit/test_file_access.py -v
python -m unittest tests/unit/test_udp_adapter.py -v
python -m unittest tests/unit/test_transfer_manager.py -v
```

### Testes de integração (requer servidor TFTP ativo)
```bash
# Com Tftpd64 rodando localmente (127.0.0.1:69)
python tests/integration/test_tftpd64.py

# Esperado:
# --- INICIANDO TESTE DE INTEGRAÇÃO REAL ---
# SUCESSO! Arquivo 'download_da_integracao.txt' criado.
# [*] Conteúdo recebido: 'Oi isso é um teste!'
# --- FIM DO TESTE ---
```

---

## Evidências de testes

### Teste de integração com Tftpd64 (servidor externo Windows)
> PUT e GET funcionando contra o servidor Tftpd64 via `127.0.0.1:69`
<img width="2559" height="1523" alt="image" src="https://github.com/user-attachments/assets/95b217e1-4e42-47b0-bfd8-2ec46bdf5308" />
<img width="2553" height="1533" alt="image" src="https://github.com/user-attachments/assets/89f22454-cad8-4f60-9229-9fe18bc1055d" />

---

## Papéis e Responsabilidades

### Arquiteto - Fernando Luis
- Elaboração dos diagramas C4
- Estrutura inicial do repositório
- Revisão e aprovação de Pull Requests

### Engenheiro de Redes e Testes - Ryan da Silva Marinho
- Criação do `README.md`
- Implementação de `udp_adapter.py`, `file_access.py`, `packet_api.py`, `client.py`, `cli.py`, `transfer_manager.py`

### Revisor e tester - Gustavo Almada
- Criação do `INTERFACE.md` e `README.md`
- Revisão e aprovação de Pull Requests.
- Execução de testes e Implementação de `test_tftpd64.py`, `test_file_access.py`, `test_packet_apy.py`, `test_transfer_manager.py`, `test_udp.py`.
---

## Referências

- [RFC 1350 — TFTP Protocol](https://datatracker.ietf.org/doc/html/rfc1350)
- [Wikipedia — TFTP](https://en.wikipedia.org/wiki/Trivial_File_Transfer_Protocol)
