import unittest
import socket
import threading
import sys
import os

# Ajuste para o Python encontrar a pasta src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from tftp_client.udp_adapter import UDPSocketAdapter
from tftp_client.errors import NetworkError

class TestUDPAdapter(unittest.TestCase):

    def setUp(self):
        self.adapter = UDPSocketAdapter(timeout=1.0)
        self.host = "127.0.0.1"
        self.port = 9999 # Porta de teste

    def tearDown(self):
        self.adapter.close()

    def test_send_and_receive_raw_bytes(self):
        """Testa se o adaptador consegue enviar e receber bytes puros."""
        msg_enviada = b"\x00\x01teste\x00octet\x00"
        msg_resposta = b"\x00\x03\x00\x01dados"

        # Criamos um servidor UDP temporário para responder ao adaptador
        def fake_server():
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.bind((self.host, self.port))
                data, addr = s.recvfrom(1024)
                if data == msg_enviada:
                    s.sendto(msg_resposta, addr)

        server_thread = threading.Thread(target=fake_server)
        server_thread.start()

        # Executa o envio pelo adaptador
        self.adapter.send(msg_enviada, self.host, self.port)
        
        # Tenta receber a resposta
        dados, addr = self.adapter.receive()
        
        self.assertEqual(dados, msg_resposta)
        self.assertEqual(addr[0], self.host)
        print("Envio e Recebimento UDP: OK")

    def test_timeout_exception(self):
        """Verifica se o adaptador levanta NetworkError em caso de silêncio do servidor."""
        with self.assertRaises(NetworkError):
            # Tenta receber sem nenhum servidor rodando
            self.adapter.receive()
        print("Tratamento de Timeout: OK")

if __name__ == '__main__':
    unittest.main()