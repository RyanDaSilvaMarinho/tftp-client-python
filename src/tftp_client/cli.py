"""
CLI / Argument Parser — Component: Python
Lê argumentos do terminal, valida parâmetros e inicia o fluxo do cliente.

Restrições:
  - NÃO acessa rede
  - NÃO acessa disco
  - NÃO manipula pacotes
"""
import argparse
import sys

from tftp_client.transfer_manager import TransferManager
from tftp_client.errors import TFTPError


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        prog="tftp-client",
        description="Cliente TFTP — RFC 1350",
        epilog=(
            "Exemplos:\n"
            "  tftp-client get 192.168.0.1 69 arquivo.txt\n"
            "  tftp-client put 192.168.0.1 69 arquivo.txt\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("operation", choices=["get", "put"])
    parser.add_argument("host")
    parser.add_argument("port", type=int)
    parser.add_argument("filename")
    parser.add_argument("--local", dest="local_path", default=None)
    parser.add_argument("--timeout", type=float, default=5.0)
    return parser.parse_args(args)


def main(args=None):
    parsed     = parse_args(args)
    local_path = parsed.local_path or parsed.filename
    manager    = TransferManager(parsed.host, parsed.port, timeout=parsed.timeout)

    try:
        if parsed.operation == "get":
            print(f"[GET] {parsed.host}:{parsed.port} → '{parsed.filename}' → '{local_path}'")
            manager.get(parsed.filename, local_path)
            print(f"[OK] Arquivo '{local_path}' recebido com sucesso.")
        else:
            print(f"[PUT] '{local_path}' → {parsed.host}:{parsed.port} → '{parsed.filename}'")
            manager.put(local_path, parsed.filename)
            print(f"[OK] Arquivo '{parsed.filename}' enviado com sucesso.")
    except TFTPError as e:
        print(f"[ERRO] {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        manager.close()