"""
UDP Socket Adapter — Component: Python
Encapsula bind, envio, recebimento e timeout de comunicação UDP.

Restrições:
  - NÃO interpreta protocolo TFTP
  - NÃO acessa disco
  - NÃO decide fluxo da transferência
"""
import socket

from tftp_client.errors import NetworkError


class UDPSocketAdapter:

    def __init__(self, timeout: float = 5.0):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.settimeout(timeout)

    def send(self, data: bytes, host: str, port: int) -> None:
        try:
            self._sock.sendto(data, (host, port))
        except OSError as e:
            raise NetworkError(f"Falha ao enviar dados para {host}:{port} — {e}")

    def receive(self, buffer_size: int = 516) -> tuple:
        try:
            data, addr = self._sock.recvfrom(buffer_size)
            return data, addr
        except socket.timeout:
            raise NetworkError("Timeout: sem resposta do servidor.")
        except OSError as e:
            raise NetworkError(f"Falha ao receber dados — {e}")

    def close(self) -> None:
        self._sock.close()