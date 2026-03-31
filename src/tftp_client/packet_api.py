"""
TFTP Packet API — Component: Python
Monta, desmonta e valida pacotes TFTP conforme RFC 1350.

Restrições:
  - NÃO acessa rede
  - NÃO acessa disco
  - NÃO controla fluxo da aplicação
"""
import struct

from tftp_client.errors import ProtocolError

# Opcodes conforme RFC 1350
OPCODE_RRQ   = 1
OPCODE_WRQ   = 2
OPCODE_DATA  = 3
OPCODE_ACK   = 4
OPCODE_ERROR = 5

ERROR_MESSAGES = {
    0: "Not defined",
    1: "File not found",
    2: "Access violation",
    3: "Disk full or allocation exceeded",
    4: "Illegal TFTP operation",
    5: "Unknown transfer ID",
    6: "File already exists",
    7: "No such user",
}


def build_rrq(filename: str, mode: str = "octet") -> bytes:
    return (
        struct.pack("!H", OPCODE_RRQ)
        + filename.encode() + b"\x00"
        + mode.encode()    + b"\x00"
    )


def build_wrq(filename: str, mode: str = "octet") -> bytes:
    return (
        struct.pack("!H", OPCODE_WRQ)
        + filename.encode() + b"\x00"
        + mode.encode()    + b"\x00"
    )


def build_data(block_number: int, data: bytes) -> bytes:
    if not (0 <= len(data) <= 512):
        raise ProtocolError(
            f"Bloco de dados deve ter entre 0 e 512 bytes, recebeu {len(data)}."
        )
    return struct.pack("!HH", OPCODE_DATA, block_number) + data


def build_ack(block_number: int) -> bytes:
    return struct.pack("!HH", OPCODE_ACK, block_number)


def build_error(error_code: int, message: str = "") -> bytes:
    msg = message or ERROR_MESSAGES.get(error_code, "Unknown error")
    return (
        struct.pack("!HH", OPCODE_ERROR, error_code)
        + msg.encode() + b"\x00"
    )


def parse_packet(raw: bytes) -> dict:
    if len(raw) < 2:
        raise ProtocolError("Pacote muito curto para conter opcode.")

    opcode = struct.unpack("!H", raw[:2])[0]

    if opcode in (OPCODE_RRQ, OPCODE_WRQ):
        try:
            parts    = raw[2:].split(b"\x00")
            filename = parts[0].decode()
            mode     = parts[1].decode()
        except (IndexError, UnicodeDecodeError) as e:
            raise ProtocolError(f"Pacote RRQ/WRQ malformado: {e}")
        return {"opcode": opcode, "filename": filename, "mode": mode}

    elif opcode == OPCODE_DATA:
        if len(raw) < 4:
            raise ProtocolError("Pacote DATA muito curto.")
        block = struct.unpack("!H", raw[2:4])[0]
        return {"opcode": OPCODE_DATA, "block": block, "data": raw[4:]}

    elif opcode == OPCODE_ACK:
        if len(raw) < 4:
            raise ProtocolError("Pacote ACK muito curto.")
        block = struct.unpack("!H", raw[2:4])[0]
        return {"opcode": OPCODE_ACK, "block": block}

    elif opcode == OPCODE_ERROR:
        if len(raw) < 4:
            raise ProtocolError("Pacote ERROR muito curto.")
        error_code = struct.unpack("!H", raw[2:4])[0]
        message    = raw[4:].rstrip(b"\x00").decode(errors="replace")
        return {"opcode": OPCODE_ERROR, "error_code": error_code, "message": message}

    else:
        raise ProtocolError(f"Opcode desconhecido: {opcode}")