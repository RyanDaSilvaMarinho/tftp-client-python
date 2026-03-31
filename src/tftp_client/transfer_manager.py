"""
Transfer Manager — Component: Python
Controla o fluxo de get e put, coordenando os demais componentes.

Restrições:
  - NÃO acessa socket diretamente
  - NÃO acessa arquivos diretamente
  - NÃO manipula bytes de pacote diretamente
"""
from tftp_client.errors import NetworkError, ProtocolError, FileAccessError
from tftp_client.packet_api import (
    build_rrq, build_wrq, build_data, build_ack, build_error,
    parse_packet,
    OPCODE_DATA, OPCODE_ACK, OPCODE_ERROR,
)
from tftp_client.udp_adapter import UDPSocketAdapter
from tftp_client.file_access import FileAccess


class TransferManager:

    def __init__(self, host: str, port: int, timeout: float = 5.0):
        self.host    = host
        self.port    = port
        self._socket = UDPSocketAdapter(timeout=timeout)
        self._file   = FileAccess()

    def get(self, remote_filename: str, local_filepath: str) -> None:
        open(local_filepath, "wb").close()
        self._socket.send(build_rrq(remote_filename), self.host, self.port)
        expected_block = 1

        while True:
            raw, server_addr = self._socket.receive()
            packet = parse_packet(raw)

            if packet["opcode"] == OPCODE_ERROR:
                raise ProtocolError(
                    f"Servidor retornou ERROR {packet['error_code']}: {packet['message']}"
                )
            if packet["opcode"] != OPCODE_DATA:
                raise ProtocolError(f"Esperava DATA, recebi opcode {packet['opcode']}.")
            if packet["block"] != expected_block:
                raise ProtocolError(
                    f"Bloco fora de ordem: esperado {expected_block}, "
                    f"recebido {packet['block']}."
                )

            self._file.write_chunk(local_filepath, packet["data"])
            self._socket.send(
                build_ack(expected_block), server_addr[0], server_addr[1]
            )

            if len(packet["data"]) < 512:
                break
            expected_block += 1

    def put(self, local_filepath: str, remote_filename: str) -> None:
        self._socket.send(build_wrq(remote_filename), self.host, self.port)
        raw, server_addr = self._socket.receive()
        packet = parse_packet(raw)

        if packet["opcode"] == OPCODE_ERROR:
            raise ProtocolError(
                f"Servidor retornou ERROR {packet['error_code']}: {packet['message']}"
            )
        if packet["opcode"] != OPCODE_ACK or packet["block"] != 0:
            raise ProtocolError("Esperava ACK 0 após WRQ.")

        block_number = 1
        for chunk in self._file.read_chunks(local_filepath):
            self._socket.send(
                build_data(block_number, chunk), server_addr[0], server_addr[1]
            )
            raw, server_addr = self._socket.receive()
            packet = parse_packet(raw)

            if packet["opcode"] == OPCODE_ERROR:
                raise ProtocolError(
                    f"Servidor retornou ERROR {packet['error_code']}: {packet['message']}"
                )
            if packet["opcode"] != OPCODE_ACK or packet["block"] != block_number:
                raise ProtocolError(
                    f"ACK inesperado: esperado bloco {block_number}."
                )
            block_number += 1

    def close(self) -> None:
        self._socket.close()