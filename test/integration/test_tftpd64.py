import os
import sys

# [ARQUITETURA] Garante que o Python encontre a pasta 'src' onde está seu código
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from tftp_client.transfer_manager import TransferManager
from tftp_client.errors import TFTPError

def test_real_integration():
    host = "127.0.0.1"
    port = 69
    remote_file = "teste.txt.txt"
    local_file = "download_da_integracao.txt"

    print(f"--- INICIANDO TESTE DE INTEGRAÇÃO REAL ---")
    
    # TESTA: O CONSTRUTOR DO TransferManager
    # Aqui ele instancia internamente o 'UDPSocketAdapter' e o 'FileAccess'.
    # Se houver erro de permissão ou porta ocupada, o erro estoura aqui.
    manager = TransferManager(host, port, timeout=2.0)
    
    try:
        if os.path.exists(local_file):
            os.remove(local_file)

        # TESTA: O MÉTODO 'get' (A ORQUESTRAÇÃO PRINCIPAL)
        # Este método é o "maestro". Ele chama as seguintes funções em ordem:
        #  - packet_api.build_rrq(): Para criar o pacote de pedido.
        #  - udp_adapter.send(): Para disparar o pacote pela rede.
        #  - udp_adapter.receive(): Para esperar o bloco vindo do Tftpd64.
        manager.get(remote_file, local_file)
        
        # TESTA: A LÓGICA DE LOOP E GRAVAÇÃO
        # Durante o manager.get(), ele testou:
        #  - packet_api.parse_packet(): Para abrir o pacote DATA recebido.
        #  - file_access.write_chunk(): Para salvar os bytes no seu HD.
        #  - packet_api.build_ack(): Para criar o pacote de confirmação.
        #  - A condição 'if len(data) < 512': Para saber que o arquivo acabou.
        
        print(f"SUCESSO! Arquivo '{local_file}' criado.")
        
        # TESTA: A INTEGRIDADE DOS DADOS
        with open(local_file, "r") as f:
            conteudo = f.read()
            print(f"[*] Conteúdo recebido: '{conteudo}'")

    except TFTPError as e:
        # TESTA: O SISTEMA DE ERROS (errors.py)
        # Se o Tftpd64 retornar "File Not Found", o ProtocolError é capturado e tratado aqui.
        print(f"FALHA NO TESTE: {e}")
        
    except Exception as e:
        # Captura erros inesperados que não são do protocolo (ex: falta de memória)
        print(f"ERRO INESPERADO: {e}")
        
    finally:
        # TESTA: O MÉTODO 'close'
        # Garante que o 'udp_adapter.close()' seja chamado para liberar o socket.
        manager.close()
        print("--- FIM DO TESTE ---")
if __name__ == "__main__":
    test_real_integration()

    