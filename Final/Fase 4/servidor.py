import socket
import json
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
    print("Servidor UDP iniciado na porta 3002") 
    
    while True:
        data, addr = server.recvfrom(2048)
        if data: 
                quadro_dict, valido = Quadro.deserializar(data)
                
                if not valido or quadro_dict is None:
                    print("[Servidor]: Quadro corrompido, descartando")
                    continue
                
                pacote = quadro_dict['data']
                segmento = pacote['data']

                seq = segmento ['seq_num']
                payload = segmento['payload']

                username = payload['username']
                message = payload ['message']

                if seq == except_seq:
                        print(f'Pacote recebido do cliente {username} com seq {seq}')

                        segmento_ack = Segmento(seq, True, None).to_dict()
                        pacote_ack = Pacote(pacote['dst_vip'], pacote['src_vip'], 3, segmento_ack).to_dict()
                        quadro_ack = Quadro(macs['SERVER_A'], macs['ROTEADOR_B'], pacote_ack).serializar()
                        enviar_pela_rede_ruidosa(server, quadro_ack, local['ROTEADOR_B'])

                        print(f'\r{username}: {message}')
                        except_seq = 1 if except_seq == 0 else 0

                else:
                        print('Pacote duplicado, reenviando ack')
                        segmento_ack = Segmento(seq, True, None).to_dict()
                        pacote_ack = Pacote(pacote['dst_vip'], pacote['src_vip'], 3, segmento_ack).to_dict()
                        quadro_ack = Quadro(macs['SERVER_A'], macs['ROTEADOR_B'], pacote_ack).serializar()
                        enviar_pela_rede_ruidosa(server, quadro_ack, local['ROTEADOR_B'])
                       
                 

main()
