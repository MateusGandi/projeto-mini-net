import socket
import json
from protocol import Segmento, Pacote

except_seq = 0

local ={
      'SERVER_A': ('localhost', 3002),
      'ROTEADOR': ('localhost', 4000)
}

def main():
    global except_seq
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(local['SERVER_A'])
    print("Servidor UDP iniciado na porta 3002") 
    
    while True:
        data, addr = server.recvfrom(2048)
        if data:
                pacote = json.loads(data.decode('utf-8'))
                segmento = pacote['data']

                seq = segmento ['seq_num']
                payload = segmento['payload']

                username = payload['username']
                message = payload ['message']

                if seq == except_seq:
                        print(f'Pacote recebido do cliente {username} com seq {seq}')

                        segmento_ack = Segmento(seq, True, None).to_dict()
                        pacote_ack = Pacote(pacote['dst_vip'], pacote['src_vip'], 10, segmento_ack).to_dict()
                        
                        server.sendto(json.dumps(pacote_ack).encode('utf-8'), addr)

                        print(f'\r{username}: {message}')
                        except_seq = 1 if except_seq == 0 else 0

                else:
                        print('Seq errado, abandonando pacote')
                 

main()
