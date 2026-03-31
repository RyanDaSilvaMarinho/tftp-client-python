import unittest
import os
import sys

# Ajuste de caminho para localizar o src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from tftp_client.file_access import FileAccess
from tftp_client.errors import FileAccessError

class TestFileAccess(unittest.TestCase):

    def setUp(self):
        """Configuração antes de cada teste."""
        self.fa = FileAccess()
        self.test_file = "test_unit_disk.bin"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        """Limpeza após cada teste."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_write_and_read_chunks(self):
        """Testa se o componente grava e lê pedaços de 512 bytes corretamente."""
        # Criando 1024 bytes (2 blocos de 512)
        dados_originais = os.urandom(1024)
        
        # Simula a chegada de dois pacotes DATA do TFTP
        self.fa.write_chunk(self.test_file, dados_originais[:512])
        self.fa.write_chunk(self.test_file, dados_originais[512:])
        
        # Lê de volta usando o generator
        dados_lidos = b"".join(list(self.fa.read_chunks(self.test_file, chunk_size=512)))
        
        self.assertEqual(dados_originais, dados_lidos)
        print("Escrita e leitura de blocos: OK")

    def test_invalid_path(self):
        """Verifica se o componente explode o erro correto para pastas inexistentes."""
        with self.assertRaises(FileAccessError):
            self.fa.validate_path("pasta_que_nao_existe/arquivo.txt")
        print("Validação de caminho inexistente: OK")

if __name__ == '__main__':
    unittest.main()