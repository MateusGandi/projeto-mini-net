import socket
import threading
import json

def handle_client(client, addr):
    print(f'Cliente conectado: {addr}')
    try:
        while True:
            data = client.recv(2048)
            if data:
                body = json.loads(data.decode('utf-8'))
                print(f'\r{body["username"]}: {body["message"]}') 

    except:
        pass
    finally:
        client.close()
        print(f'Cliente desconectado: {addr}')

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    print("Servidor iniciado na porta 3000")

    try:
        server.bind(("localhost", 3000))
    except:
        return print('\nNão foi possível iniciar o servidor!\n')

    server.listen(1)
    
    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()

main()
