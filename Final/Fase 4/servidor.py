import socket
from color import c_print, Colors, Layers
from protocol import Segmento, Pacote, Quadro, enviar_pela_rede_ruidosa

except_seq = 0

local = {
    'SERVER_A': ('localhost', 3002),
    'ROTEADOR_B': ('localhost', 4001)
}

macs = {
    'SERVER_A': '00:00:00:00:00:04',
    'ROTEADOR_B': '00:00:00:00:00:03',
}

def main():
    global except_seq

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(local['SERVER_A'])
    c_print("Servidor UDP iniciado na porta 3002", Colors.AZUL, layer=Layers.APLICACAO)

    while True:
        data, addr = server.recvfrom(2048)

        if not data:
            continue 
        
        c_print("Quadro recebido, iniciando desserialização", Colors.VERMELHO, layer=Layers.ENLACE)

        quadro_dict, valido = Quadro.deserializar(data)

        if not valido or quadro_dict is None:
            c_print("Quadro corrompido, descartando", Colors.VERMELHO, layer=Layers.ENLACE)
            continue

        c_print("Quadro íntegro, extraindo pacote", Colors.VERMELHO, layer=Layers.ENLACE)
 
        pacote = quadro_dict['data']

        c_print(f"Pacote recebido: origem VIP={pacote['src_vip']} destino VIP={pacote['dst_vip']} TTL={pacote['ttl']}",
                Colors.VERDE, layer=Layers.REDE)

        segmento = pacote['data']
 
        seq = segmento['seq_num']
        payload = segmento['payload']
        is_ack = segmento['is_ack']

        c_print(f"Segmento recebido: seq={seq} is_ack={is_ack}", 
                Colors.AMARELO, layer=Layers.TRANSPORTE)

        if is_ack:
            c_print("Segmento é ACK. Servidor ignora.", 
                    Colors.AMARELO, layer=Layers.TRANSPORTE)
            continue

        username = payload['username']
        message = payload['message'] 
 
        if seq == except_seq:

            c_print(f"Seq esperada ({except_seq}) recebida. Aceitando pacote.", 
                    Colors.AMARELO, layer=Layers.TRANSPORTE)
 
            c_print("Criando segmento ACK", 
                    Colors.AMARELO, layer=Layers.TRANSPORTE)

            segmento_ack = Segmento(seq, True, None).to_dict()
 
            c_print("Invertendo VIP origem/destino para resposta", 
                    Colors.VERDE, layer=Layers.REDE)

            pacote_ack = Pacote(
                pacote['dst_vip'],
                pacote['src_vip'],
                3,
                segmento_ack
            ).to_dict() 

            c_print("Encapsulando pacote ACK em quadro", 
                    Colors.VERMELHO, layer=Layers.ENLACE)

            quadro_ack = Quadro(
                macs['SERVER_A'],
                macs['ROTEADOR_B'],
                pacote_ack
            ).serializar()
 
            enviar_pela_rede_ruidosa(server, quadro_ack, local['ROTEADOR_B'])
 
            c_print(f'{username}: {message}', 
                    Colors.AZUL, layer=Layers.APLICACAO)
 
            except_seq = 1 if except_seq == 0 else 0

            c_print(f"Próxima sequência esperada: {except_seq}", 
                    Colors.AMARELO, layer=Layers.TRANSPORTE)

        else:

            c_print("Pacote duplicado detectado (seq inesperada)", 
                    Colors.AMARELO, layer=Layers.TRANSPORTE)

            c_print("Reenviando ACK anterior", 
                    Colors.AMARELO, layer=Layers.TRANSPORTE)

            segmento_ack = Segmento(seq, True, None).to_dict()

            pacote_ack = Pacote(
                pacote['dst_vip'],
                pacote['src_vip'],
                3,
                segmento_ack
            ).to_dict()

            quadro_ack = Quadro(
                macs['SERVER_A'],
                macs['ROTEADOR_B'],
                pacote_ack
            ).serializar()

            enviar_pela_rede_ruidosa(server, quadro_ack, local['ROTEADOR_B'])


main()