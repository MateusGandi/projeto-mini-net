import socket
import json
from protocol import Quadro, enviar_pela_rede_ruidosa

# tabela de roteamento
local = {
    'HOST_A': ('localhost', 3001),
    'SERVER_A': ('localhost', 3002), 
    'SERVER_B': ('localhost', 3004),
    'ROTEADOR_A': ('localhost', 4000),
    'ROTEADOR_B': ('localhost', 4001)
}
macs = { 
    'HOST_A': '00:00:00:00:00:01',
    'ROTEADOR_A': '00:00:00:00:00:02', 
    'ROTEADOR_B': '00:00:00:00:00:03',
    'SERVER_A': '00:00:00:00:00:04',
    'SERVER_B': '00:00:00:00:00:05',
}
 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(local['ROTEADOR_B'])
print("Roteador B UDP iniciado na porta 4001")

while True:
    data, addr = sock.recvfrom(4096)
    quadro_dict, valido = Quadro.deserializar(data)
    
    if not valido or quadro_dict is None:
        print("[Roteador B]: Quadro corrompido, descartando")
        continue
    
    pacote = quadro_dict['data']
 
    pacote["ttl"] -= 1

    if pacote["ttl"] <= 0:
        print("Pacote expirado")
        continue 

    destino_virtual = pacote["dst_vip"]

    if destino_virtual in local:
        ip, porta = local[destino_virtual]

        print(f"[Roteador B]: Enviando pacote de {pacote['src_vip']} para {destino_virtual}")
        new_quadro = Quadro(macs['ROTEADOR_B'], macs[destino_virtual], pacote).serializar()
        enviar_pela_rede_ruidosa(sock, new_quadro, (ip, porta))
    else:
        print("Destino desconhecido")