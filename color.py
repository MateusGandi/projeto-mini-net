class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'

    PRETO = '\033[30m' #FISICA
    VERMELHO = '\033[31m'  #ENLACE
    VERDE = '\033[32m' #REDE
    AMARELO = '\033[33m' #TRANSPORTE
    AZUL = '\033[34m' #APLICACAO
    MAGENTA = '\033[35m'
    CIANO = '\033[36m'
    BRANCO = '\033[37m'

    PRETO_BRIGHT = '\033[90m'
    VERMELHO_BRIGHT = '\033[91m'
    VERDE_BRIGHT = '\033[92m'
    AMARELO_BRIGHT = '\033[93m'
    AZUL_BRIGHT = '\033[94m'
    MAGENTA_BRIGHT = '\033[95m'
    CIANO_BRIGHT = '\033[96m'
    BRANCO_BRIGHT = '\033[97m'

    FUNDO_PRETO = '\033[40m'
    FUNDO_VERMELHO = '\033[41m'
    FUNDO_VERDE = '\033[42m'
    FUNDO_AMARELO = '\033[43m'
    FUNDO_AZUL = '\033[44m'
    FUNDO_MAGENTA = '\033[45m'
    FUNDO_CIANO = '\033[46m'
    FUNDO_BRANCO = '\033[47m'


class Layers :
    APLICACAO = 'APLICACAO'
    TRANSPORTE = 'TRANSPORTE'
    REDE = 'REDE'
    ENLACE = 'ENLACE'
    FISICA = 'FÍSICA'

def c_print(texto, cor=Colors.BRANCO, fundo=None, estilo=None, reset=True, layer=None):
    texto_alterado = texto

    if layer:
        texto_alterado = f'   [{layer}] {texto}'

    if fundo:
        print(f"{estilo or ''}{cor}{fundo}{texto_alterado}", end='')
    else:
        print(f"{estilo or ''}{cor}{texto_alterado}", end='')

    if reset:
        print(Colors.RESET)
    else:
        print()



# colored_print("Texto vermelho", Colors.VERMELHO)
# colored_print("Texto verde brilhante", Colors.VERDE_BRIGHT)
# colored_print("Texto azul com fundo amarelo", Colors.AZUL, Colors.FUNDO_AMARELO)
# colored_print("Texto em negrito magenta", Colors.MAGENTA, estilo=Colors.BOLD)