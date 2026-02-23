import threading
import socket
import json
from protocol import Segmento, Pacote

seq = 0
timeout = 3 
local ={
    'HOST_A': ('localhost', 3001),
    'ROTEADOR': ('localhost', 4000)
} 
#'SERVER_A', -> ('localhost', 3002),
#'SERVER_B' -> ('localhost', 3004),
 
def check_ack(pacote_received):
    segmento_received = pacote_received['data']
    is_ack  = segmento_received['is_ack']
    seq_received = segmento_received['seq_num']

    return is_ack and seq_received == seq
 

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind(local['HOST_A'])

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
                server = 'SERVER_B' if msg == 'teste' else 'SERVER_A'
                pacote = Pacote('HOST_A', server, 0, segmento).to_dict()
 
                client.sendto(json.dumps(pacote).encode('utf-8'), local['ROTEADOR'])
                while True:
                    if tentativas > 2:
                        print(f'\nFalha ao enviar a mensagem "{msg}" após 3 tentativas. Abortando...\n')
                        break

                    client.settimeout(timeout)
                    try:
                        data, addr = client.recvfrom(2048)
                        if data:
                            pacote_received = json.loads(data.decode('utf-8'))

                            if check_ack(pacote_received):
                                print(f'Ack recebido para: {seq}') 
                                seq = 1 if seq == 0 else 0
                                print(f'Mensagem enviada com sucesso!')
                                break
 

                    except socket.timeout:
                        tentativas += 1
                        print(f'\nTimeout: Não recebeu ACK para a mensagem "{msg}". Tentando novamente...\n')
                        client.sendto(json.dumps(pacote).encode('utf-8'), local['ROTEADOR'])
        except Exception as e:
            print(f'\nErro ao enviar mensagem: {e}\n')
            client.close()
            break  
            

main()
