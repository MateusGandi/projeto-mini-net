import socket
from color import c_print, Colors, Layers
from protocol import Quadro, enviar_pela_rede_ruidosa 

local = {
    'HOST_A': ('localhost', 3001), 
    'ROTEADOR_A': ('localhost', 4000),
    'ROTEADOR_B': ('localhost', 4001)
}

macs = {
    'HOST_A': '00:00:00:00:00:01',
    'ROTEADOR_A': '00:00:00:00:00:02', 
    'ROTEADOR_B': '00:00:00:00:00:03',
}
 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(local['ROTEADOR_A'])
c_print("Roteador A iniciado", Colors.VERDE, layer=Layers.REDE)

while True:
    data, addr = sock.recvfrom(4096)

    c_print('Desencapsulando quadro recebido', Colors.VERMELHO, layer=Layers.ENLACE)
    quadro_dict, valido = Quadro.deserializar(data)
    
    if not valido or quadro_dict is None:
        c_print("Quadro inválido descartado", Colors.VERMELHO, layer=Layers.ENLACE)
        continue
    
    c_print('Extraindo pacote IP', Colors.VERDE, layer=Layers.REDE)
    pacote = quadro_dict['data']

    c_print('Decrementando TTL', Colors.VERDE, layer=Layers.REDE)
    pacote["ttl"] -= 1

    if pacote["ttl"] <= 0:
        c_print("Pacote expirado (TTL=0)", Colors.VERDE, layer=Layers.REDE)
        continue 

    destino_virtual = pacote["dst_vip"]
    c_print(f'Consultando tabela de roteamento para {destino_virtual}', Colors.VERDE, layer=Layers.REDE)

    if destino_virtual in local:
        ip, porta = local[destino_virtual]

        c_print('Reencapsulando pacote com novos MACs', Colors.VERMELHO, layer=Layers.ENLACE)
        new_quadro = Quadro(macs['ROTEADOR_A'], macs[destino_virtual], pacote).serializar()

        c_print('Encaminhando para próximo salto', Colors.VERDE, layer=Layers.REDE)
        enviar_pela_rede_ruidosa(sock, new_quadro, (ip, porta))
    else:
        c_print('Destino não local - encaminhando para Roteador B', Colors.VERDE, layer=Layers.REDE)
        new_quadro = Quadro(macs['ROTEADOR_A'], macs['ROTEADOR_B'], pacote).serializar()
        enviar_pela_rede_ruidosa(sock, new_quadro, local['ROTEADOR_B'])