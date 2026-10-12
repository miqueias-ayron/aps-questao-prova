"""Janela, eventos de teclado e mouse, e o laço principal da animação."""

import pygame

from .tipografia import Fontes
from .grid import DesenhoGrid
from .telas import desenhar_tela_mundo, desenhar_tela_entrada

TELA_CHEIA_INICIAL = True
TAMANHO_JANELA = (1280, 800)
INTERVALO_MS = 400


def montar_caminho(resultado):
    if resultado is None:
        return None

    nodos = []
    nodo = resultado
    while nodo is not None:
        nodos.append(nodo)
        nodo = nodo.father_node
    return list(reversed(nodos))


def abrir_tela(tela_cheia):
    if tela_cheia:
        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    return pygame.display.set_mode(TAMANHO_JANELA, pygame.RESIZABLE)


def executar(novo_mundo, tamanho_minimo, tamanho_maximo):
    # novo_mundo(n) gera um mundo n x n, faz a busca e retorna (resultado, agente_inicial, produto_inicial)
    pygame.init()
    pygame.display.set_caption('Entrega com A*')
    fontes = Fontes()
    desenho_grid = DesenhoGrid()
    relogio = pygame.time.Clock()
    tela_cheia = TELA_CHEIA_INICIAL
    tela = abrir_tela(tela_cheia)

    na_entrada = True
    texto_digitado = ''
    erro = ''
    botoes = {}
    n = None
    caminho = None
    agente_inicial = produto_inicial = None
    passo = 0
    pausado = False
    ultimo_passo = 0

    def gerar():
        nonlocal n, caminho, agente_inicial, produto_inicial, na_entrada, passo, pausado, ultimo_passo, erro
        if texto_digitado.isdigit() and tamanho_minimo <= int(texto_digitado) <= tamanho_maximo:
            n = int(texto_digitado)
            resultado, agente_inicial, produto_inicial = novo_mundo(n)
            caminho = montar_caminho(resultado)
            na_entrada = False
            passo, pausado, ultimo_passo = 0, False, pygame.time.get_ticks()
        else:
            erro = f'Digite um número inteiro entre {tamanho_minimo} e {tamanho_maximo}'

    def ajustar(delta):
        nonlocal texto_digitado, erro
        atual = int(texto_digitado) if texto_digitado.isdigit() else tamanho_minimo - delta
        texto_digitado = str(min(tamanho_maximo, max(tamanho_minimo, atual + delta)))
        erro = ''

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and na_entrada:
                if botoes.get('diminuir') and botoes['diminuir'].collidepoint(evento.pos):
                    ajustar(-1)
                elif botoes.get('aumentar') and botoes['aumentar'].collidepoint(evento.pos):
                    ajustar(1)
                elif botoes.get('gerar') and botoes['gerar'].collidepoint(evento.pos):
                    gerar()
            elif evento.type != pygame.KEYDOWN:
                continue
            elif evento.key == pygame.K_ESCAPE:
                rodando = False
            elif evento.key == pygame.K_F11:
                tela_cheia = not tela_cheia
                tela = abrir_tela(tela_cheia)
            elif na_entrada:
                if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    gerar()
                elif evento.key == pygame.K_BACKSPACE:
                    texto_digitado = texto_digitado[:-1]
                    erro = ''
                elif evento.key == pygame.K_UP:
                    ajustar(1)
                elif evento.key == pygame.K_DOWN:
                    ajustar(-1)
                elif evento.unicode.isdigit() and len(texto_digitado) < 3:
                    texto_digitado += evento.unicode
                    erro = ''
            else:
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado
                elif evento.key == pygame.K_r:
                    passo, ultimo_passo = 0, pygame.time.get_ticks()
                elif evento.key == pygame.K_n:
                    resultado, agente_inicial, produto_inicial = novo_mundo(n)
                    caminho = montar_caminho(resultado)
                    passo, pausado, ultimo_passo = 0, False, pygame.time.get_ticks()
                elif evento.key == pygame.K_d:
                    na_entrada = True
                    texto_digitado, erro = str(n), ''

        tela = pygame.display.get_surface()
        if na_entrada:
            botoes = desenhar_tela_entrada(tela, fontes, texto_digitado, erro, tamanho_minimo, tamanho_maximo)
        else:
            if caminho and not pausado and passo < len(caminho) - 1:
                agora = pygame.time.get_ticks()
                if agora - ultimo_passo >= INTERVALO_MS:
                    passo += 1
                    ultimo_passo = agora
            desenhar_tela_mundo(tela, fontes, desenho_grid, caminho, passo, pausado, agente_inicial, produto_inicial)

        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()