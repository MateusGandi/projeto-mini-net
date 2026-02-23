import socket
import json
from protocol import Segmento

except_seq = 0

def main():
    global except_seq
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    print("Servidor UDP iniciado na porta 3000")

    try:
        server.bind(("localhost", 3000))
    except:
        return print('\nNão foi possível iniciar o servidor!\n')
    
    while True:
        data, addr = server.recvfrom(2048)
        if data:
                segmento = json.loads(data.decode('utf-8'))
                seq = segmento.get('seq_num')
                body = segmento.get('payload')
                username = body.get('username')
                message = body.get('message')

                if seq == except_seq:
                        print(f'Pacote recebido do cliente {username} com seq {seq}')
                        segmento_ack = Segmento(seq, True, None).to_dict()
                        server.sendto(json.dumps(segmento_ack).encode('utf-8'), addr)
                        print(f'\r{username}: {message}')
                        except_seq = 1 if except_seq == 0 else 0

                else:
                        print('Seq errado, abandonando pacote')
                 

main()
