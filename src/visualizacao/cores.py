"""Paleta de cores da interface (tema escuro)."""


def cor(hexa):
    hexa = hexa.lstrip('#')
    return tuple(int(hexa[i:i + 2], 16) for i in (0, 2, 4))


def misturar(a, b, t):
    # t = 0 devolve b, t = 1 devolve a
    return tuple(round(a[i] * t + b[i] * (1 - t)) for i in range(3))


FUNDO = cor('#0F1419')
PAINEL = cor('#161C23')
BORDA = cor('#26303A')
CARTAO = cor('#1C242D')
MOLDURA_GRID = cor('#141A21')
LIVRE = cor('#1E2730')
OBSTACULO = cor('#4A5664')
OBSTACULO_SOMBRA = cor('#36404C')
PEDAGIO_CLARO = cor('#3A2F1C')
PEDAGIO_ESCURO = cor('#2C2618')
PEDAGIO_BORDA = cor('#C98A2B')
TEXTO = cor('#E6EBF0')
TEXTO_2 = cor('#9AA7B4')
TEXTO_3 = cor('#6E7C8A')
TEXTO_LEGENDA = cor('#C3CCD5')
DESTAQUE = cor('#4CC9F0')
DESTAQUE_TEXTO = cor('#7FD8F5')
DESTAQUE_FUNDO = cor('#12313D')
PRODUTO = cor('#F28C38')
PRODUTO_ESCURO = cor('#B85E17')
PRODUTO_TEXTO = cor('#F5A65F')
DESTINO = cor('#F2F4F6')
ERRO = cor('#FF8A7A')
ERRO_FUNDO = cor('#3D1E1A')
ALERTA_FUNDO = cor('#2A1916')
ALERTA_BORDA = cor('#5A2A23')
ALERTA_TITULO = cor('#FFD2CB')
ALERTA_TEXTO = cor('#E3B9B2')
SUCESSO = cor('#7BD88F')
SUCESSO_FUNDO = cor('#1A3322')
BOTAO_TEXTO = cor('#0B1A21')
BOTAO_BORDA = cor('#2E3945')
TECLA_SOMBRA = cor('#1A2129')