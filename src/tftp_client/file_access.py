"""
File Access — Component: Python
Lê arquivos locais para upload, grava arquivos recebidos e valida caminhos.

Restrições:
  - NÃO interpreta pacotes TFTP
  - NÃO acessa socket
  - NÃO controla fluxo da transferência
"""
from pathlib import Path
from typing import Generator

from tftp_client.errors import FileAccessError


class FileAccess:

    def read_chunks(
        self, filepath: str, chunk_size: int = 512
    ) -> Generator[bytes, None, None]:
        path = self.validate_path(filepath)
        try:
            with open(path, "rb") as f:
                while True:
                    chunk = f.read(chunk_size)
                    yield chunk
                    if len(chunk) < chunk_size:
                        break
        except OSError as e:
            raise FileAccessError(f"Erro ao ler '{filepath}' — {e}")

    def write_chunk(self, filepath: str, data: bytes) -> None:
        try:
            with open(filepath, "ab") as f:
                f.write(data)
        except OSError as e:
            raise FileAccessError(f"Erro ao gravar em '{filepath}' — {e}")

    def validate_path(self, filepath: str) -> Path:
        path = Path(filepath).resolve()
        if not path.parent.exists():
            raise FileAccessError(f"Diretório não encontrado: '{path.parent}'")
        return path