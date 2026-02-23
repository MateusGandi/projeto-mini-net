import threading
import socket
import json
from protocol import Segmento

seq = 0
timeout = 3 # 2 segundos 

SERVER_ADDRESS = ('localhost', 3000)
F_SERVER_ADDRESS = ('localhost', 3001)

def check_ack(pacote_received):
    segmento_received = pacote_received['data']
    is_ack  = segmento_received['is_ack']
    seq_received = segmento_received['seq_num']

    return is_ack and seq_received == seq

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    username = input('Seu nome: ')
    print('Conectado!\n')

    thread = threading.Thread(target=sendMessages, args=[client, username])
    thread.start()

def sendMessages(client, username):
    global seq
    global timeout 

    while True:
        try:
            tentativas = 0
            msg = input(f'{username}> ')
            if msg:
                segmento = Segmento(seq, False, {'username': username, 'message': msg}).to_dict()
               
                server_addr = F_SERVER_ADDRESS if msg == 'teste' else SERVER_ADDRESS

                client.sendto(json.dumps(segmento).encode('utf-8'), server_addr)
                while True:
                    if tentativas > 2:
                        print(f'\nFalha ao enviar a mensagem "{msg}" após 3 tentativas. Abortando...\n')
                        break

                    client.settimeout(timeout)
                    try:
                        data, addr = client.recvfrom(2048)
                        if data:
                            response = json.loads(data.decode('utf-8')) 

                            if check_ack(response):
                                print(f'Ack recebido para: {seq}') 
                                seq = 1 if seq == 0 else 0
                                print(f'Mensagem enviada com sucesso!')
                                break
 

                    except socket.timeout:
                        tentativas += 1
                        print(f'\nTimeout: Não recebeu ACK para a mensagem "{msg}". Tentando novamente...\n')
                        client.sendto(json.dumps(segmento).encode('utf-8'), server_addr)
        except:
            print('\nErro ao enviar mensagem!\n')
            client.close()
            break  
            

main()
