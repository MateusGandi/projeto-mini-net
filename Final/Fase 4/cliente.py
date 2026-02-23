import threading
import socket
import json
from color import c_print, Colors, Layers
from protocol import Segmento, Pacote, Quadro, enviar_pela_rede_ruidosa 

seq = 0
timeout = 10 

local = {
    'HOST_A': ('localhost', 3001),
    'ROTEADOR_A': ('localhost', 4000)
} 

macs = {
    'HOST_A': '00:00:00:00:00:01',
    'ROTEADOR_A': '00:00:00:00:00:02', 
}

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind(local['HOST_A'])

    username = input('Seu nome: ')
    c_print('Aplicação iniciada', Colors.AZUL, layer=Layers.APLICACAO)

    thread = threading.Thread(target=sendMessages, args=[client, username])
    thread.start()

def check_ack(pacote_received):
    c_print('Desmontando segmento recebido para verificar ACK', Colors.AMARELO, layer=Layers.TRANSPORTE)
    segmento_received = pacote_received['data']
    is_ack  = segmento_received['is_ack']
    seq_received = segmento_received['seq_num']
    return is_ack and seq_received == seq

def sendMessages(client, username):
    global seq
    global timeout 

    while True:
        try:
            tentativas = 0
            msg = input(f'{username}> ')
            if msg:

                c_print('Montando segmento de dados', Colors.AMARELO, layer=Layers.TRANSPORTE)
                segmento = Segmento(seq, False, {'username': username, 'message': msg}).to_dict()

                server = 'SERVER_B' if msg == 'teste' else 'SERVER_A'
                c_print(f'Definindo destino lógico: {server}', Colors.VERDE, layer=Layers.REDE)

                c_print('Montando pacote IP com TTL inicial 3', Colors.VERDE, layer=Layers.REDE)
                pacote = Pacote('HOST_A', server, 3, segmento).to_dict()

                c_print('Encapsulando pacote em quadro com endereços MAC', Colors.VERMELHO, layer=Layers.ENLACE)
                quadro = Quadro(macs['HOST_A'], macs['ROTEADOR_A'], pacote).serializar()

                c_print('Enviando quadro ao roteador', Colors.VERMELHO, layer=Layers.ENLACE)
                enviar_pela_rede_ruidosa(client, quadro, local['ROTEADOR_A'])
 
                while True:
                    if tentativas > 10:
                        c_print('Limite de retransmissões atingido', Colors.AMARELO, layer=Layers.TRANSPORTE)
                        break

                    client.settimeout(timeout)
                    try:
                        data, addr = client.recvfrom(2048)
                        if data:

                            c_print('Desencapsulando quadro recebido', Colors.VERMELHO, layer=Layers.ENLACE)
                            quadro_dict, valido = Quadro.deserializar(data)
                            
                            if not valido or quadro_dict is None:
                                c_print('Quadro inválido descartado', Colors.VERMELHO, layer=Layers.ENLACE)
                                continue
                            
                            c_print('Extraindo pacote do quadro', Colors.VERDE, layer=Layers.REDE)
                            pacote_received = quadro_dict['data']

                            if check_ack(pacote_received):
                                c_print(f'ACK válido recebido para seq {seq}', Colors.AMARELO, layer=Layers.TRANSPORTE)
                                seq = 1 if seq == 0 else 0
                                c_print('Entrega confirmada na aplicação', Colors.AZUL, layer=Layers.APLICACAO)
                                break

                    except socket.timeout:
                        tentativas += 1
                        c_print('Timeout detectado - retransmitindo', Colors.AMARELO, layer=Layers.TRANSPORTE)
                        enviar_pela_rede_ruidosa(client, quadro, local['ROTEADOR_A'])

        except Exception as e:
            c_print(f'Erro na aplicação: {e}', Colors.AZUL, layer=Layers.APLICACAO)
            client.close()
            break  

main()