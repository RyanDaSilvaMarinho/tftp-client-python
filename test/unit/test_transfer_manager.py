import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Ajuste de caminho
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from tftp_client.transfer_manager import TransferManager
from tftp_client import packet_api as api

class TestTransferManagerUnit(unittest.TestCase):

    def setUp(self):

        self.tm = TransferManager("127.0.0.1", 69)
        
        self.tm._socket.close() 
        
        self.tm._socket = MagicMock()
        self.tm._file = MagicMock()

    def tearDown(self):
        # Garante que tudo seja limpo
        self.tm.close()

    def test_get_flow_completion(self):
        """Testa se o manager encerra o GET ao receber um pacote final (< 512 bytes)."""
        dados_finais = b"Ultimos bytes"
        pacote_data = api.build_data(block_number=1, data=dados_finais)
        
        # Mock do retorno do socket: (pacote, (ip, porta))
        self.tm._socket.receive.return_value = (pacote_data, ("127.0.0.1", 50000))

        with patch("builtins.open", unittest.mock.mock_open()):
            self.tm.get("arquivo.txt", "local.txt")

        # Verificações
        self.tm._file.write_chunk.assert_called_with("local.txt", dados_finais)
        self.tm._socket.send.assert_any_call(api.build_ack(1), "127.0.0.1", 50000)
        print("✅ Fluxo de encerramento do GET: OK")

if __name__ == '__main__':
    unittest.main()