import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from tftp_client import packet_api as api

class TestPacketAPI(unittest.TestCase):

    def test_build_rrq(self):
        """Verifica se o RRQ segue o formato: Opcode(2b) + Nome + 0 + Modo + 0"""
        packet = api.build_rrq("documento.pdf")
        expected = b'\x00\x01documento.pdf\x00octet\x00'
        self.assertEqual(packet, expected)

    def test_build_ack(self):
        """Verifica se o ACK do bloco 10 está correto."""
        packet = api.build_ack(10)
        self.assertEqual(packet, b'\x00\x04\x00\x0a') # 0x0a é 10 em hex

    def test_parse_data_packet(self):
        """Simula um pacote DATA vindo da rede e verifica o parser."""
        raw_packet = b'\x00\x03\x00\x01Dados de Teste'
        parsed = api.parse_packet(raw_packet)
        self.assertEqual(parsed['opcode'], api.OPCODE_DATA)
        self.assertEqual(parsed['block'], 1)
        self.assertEqual(parsed['data'], b'Dados de Teste')

if __name__ == '__main__':
    unittest.main()