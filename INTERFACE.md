# Documentação de Interfaces

Este documento descreve a comunicação entre os módulos do cliente TFTP, utilizando a nomenclatura exata das funções implementadas no código-fonte.

---

## 1. Camada de Orquestração (`transfer_manager.py`)
Responsável por gerenciar o estado da transferência e unir a lógica de rede com a de disco.

| Função | Entrada | Saída | Responsabilidade |
| :--- | :--- | :--- | :--- |
| `get(remote_file, local_file)` | `str`, `str` | `None` | Inicia RRQ, recebe blocos e salva via `FileAccess`. |
| `put(local_file, remote_file)` | `str`, `str` | `None` | Inicia WRQ, lê via `FileAccess` e envia pacotes DATA. |
| `close()` | `None` | `None` | Encerra a conexão através do `UDPAdapter`. |

---

## 2. Camada de Protocolo (`packet_api.py`)
Módulo puramente lógico que traduz dados Python para o formato binário da **RFC 1350**.

* **`build_rrq(filename, mode)` / `build_wrq(filename, mode)`**: 
    * Retorna `bytes` contendo o Opcode (1 ou 2) + Nome do Arquivo + Modo.
* **`parse_packet(raw_bytes)`**: 
    * Decodifica datagramas brutos. Retorna um `dict` com: `opcode`, `block_num`, `data` ou `error_code`.
* **`build_ack(block_number)`**: 
    * Gera os 4 bytes de confirmação (Opcode 4 + Número do Bloco).
* **`build_data(block_number, data)`**: 
    * Gera o pacote DATA (Opcode 3 + Bloco + até 512 bytes de carga).

---

## 3. Camada de Adaptação de Rede (`udp_adapter.py`)
Isola a biblioteca padrão `socket` do Python, permitindo a troca de mensagens UDP.

* **`send(data, host, port)`**: Dispara bytes para o destino via socket UDP.
* **`receive(timeout)`**: Aguarda resposta. Retorna uma tupla `(bytes, (ip, porta))`. Lança `NetworkError` em caso de tempo esgotado.
* **`close()`**: Fecha o descritor de socket no Sistema Operacional.

---

## 4. Camada de Acesso a Arquivos (`file_access.py`)
Gerencia a persistência de dados no disco rígido de forma binária.

* **`read_chunk(filepath, chunk_size=512)`**: 
    * **Tipo:** Generator (`yield`). Lê o arquivo em pedaços para evitar consumo excessivo de RAM.
* **`write_chunk(filepath, data)`**: 
    * Abre o arquivo no modo `ab` (append binary) e anexa os dados recebidos da rede.

---

## 5. Tratamento de Exceções (`errors.py`)
Padronização das falhas que podem ocorrer durante a execução.

* **`TFTPError`**: Exceção base do sistema.
* **`NetworkError`**: Falha de conexão ou Timeout de rede.
* **`ProtocolError`**: Erro retornado pelo servidor (ex: Arquivo não encontrado).
* **`FileAccessError`**: Erro de leitura/escrita no sistema de arquivos local.

---
*Documentação gerada para o Projeto de Sistemas de Informação - 2026*