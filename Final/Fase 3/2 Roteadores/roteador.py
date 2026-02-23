import socket
import json

# tabela de roteamento
local = {
    'HOST_A': ('localhost', 3001), 
    'ROTEADOR_A': ('localhost', 4000),
    'ROTEADOR_B': ('localhost', 4001)
}
 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(local['ROTEADOR_A'])
print("Roteador A UDP iniciado na porta 4000")

while True:
    data, addr = sock.recvfrom(4096)
    pacote = json.loads(data.decode())
 
 
    pacote["ttl"] -= 1

    if pacote["ttl"] <= 0:
        print("Pacote expirado")
        continue 

    destino_virtual = pacote["dst_vip"]

    if destino_virtual in local:
        ip, porta = local[destino_virtual]

        print(f"[Roteador A]: Enviando pacote de {pacote['src_vip']} para {destino_virtual}")
        sock.sendto(json.dumps(pacote).encode(), (ip, porta))
    else:
         sock.sendto(json.dumps(pacote).encode(), local['ROTEADOR_B'])