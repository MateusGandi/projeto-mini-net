import threading
import socket
import json

SERVER_ADDRESS = ('localhost', 3000)

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(SERVER_ADDRESS)
    except:
        return print('\nNão foi possível se conectar ao servidor!\n')

    username = input('Seu nome: ')
    print('Conectado!\n')

    thread = threading.Thread(target=sendMessages, args=[client, username])
    thread.start()

def sendMessages(client, username):
    while True:
        try:
            msg = input(f'{username}> ')
            if msg:
                body = { 
                    'username': username,
                    'message': msg
                }
                client.sendto(json.dumps(body).encode('utf-8'), SERVER_ADDRESS)
             
        except:
            print('\nErro ao enviar mensagem!\n')
            client.close()
            break

main()
