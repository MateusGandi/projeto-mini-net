import threading
import socket
import json
from protocol import Segmento, Pacote, Quadro, enviar_pela_rede_ruidosa 

seq = 0
timeout = 10 
local ={
    'HOST_A': ('localhost', 3001),
    'ROTEADOR_A': ('localhost', 4000)
} 
macs = {
    'HOST_A': '00:00:00:00:00:01',
    'ROTEADOR_A': '00:00:00:00:00:02', 
}
#'SERVER_A', -> ('localhost', 3002),
#'SERVER_B' -> ('localhost', 3004),
 
 

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind(local['HOST_A'])

    username = input('Seu nome: ')
    print('Conectado!\n')

    thread = threading.Thread(target=sendMessages, args=[client, username])
    thread.start()

def check_ack(pacote_received):
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
                segmento = Segmento(seq, False, {'username': username, 'message': msg}).to_dict()
                server = 'SERVER_B' if msg == 'teste' else 'SERVER_A'
                pacote = Pacote('HOST_A', server, 3, segmento).to_dict()
                quadro = Quadro( macs['HOST_A'], macs['ROTEADOR_A'], pacote).serializar()

                enviar_pela_rede_ruidosa(client, quadro, local['ROTEADOR_A'])
 
                while True:
                    if tentativas > 10:
                        print(f'\nFalha ao enviar a mensagem "{msg}" após 3 tentativas. Abortando...\n')
                        break

                    client.settimeout(timeout)
                    try:
                        data, addr = client.recvfrom(2048)
                        if data:
                            quadro_dict, valido = Quadro.deserializar(data)
                            
                            if not valido or quadro_dict is None:
                                print("[Cliente]: Quadro corrompido, ignorando")
                                continue
                            
                            pacote_received = quadro_dict['data']

                            if check_ack(pacote_received):
                                print(f'Ack recebido para: {seq}') 
                                seq = 1 if seq == 0 else 0
                                print(f'Mensagem enviada com sucesso!')
                                break
 

                    except socket.timeout:
                        tentativas += 1
                        print(f'\nTimeout: Não recebeu ACK para a mensagem "{msg}". Tentando novamente...\n')
 
                        enviar_pela_rede_ruidosa(client, quadro, local['ROTEADOR_A'])

        except Exception as e:
            print(f'\nErro ao enviar mensagem: {e}\n')
            client.close()
            break  
            

main()
