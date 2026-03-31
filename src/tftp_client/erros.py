"""
errors.py — Exceções do domínio TFTP Client.
Todos os componentes importam daqui. Nenhuma dependência interna.
"""


class TFTPError(Exception):
    """Exceção base para todos os erros do cliente TFTP."""
    pass


class NetworkError(TFTPError):
    """Falha na comunicação UDP (timeout, socket, etc.)."""
    pass


class FileAccessError(TFTPError):
    """Falha ao ler ou gravar arquivos locais."""
    pass


class ProtocolError(TFTPError):
    """Violação do protocolo TFTP (pacote inválido, opcode inesperado, etc.)."""
    pass