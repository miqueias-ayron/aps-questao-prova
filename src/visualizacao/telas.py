"""Telas completas: escolha da dimensão e grid com painel."""

import pygame

from .cores import (
    FUNDO, PAINEL, BORDA, CARTAO, TEXTO, TEXTO_2, TEXTO_LEGENDA, DESTAQUE, PRODUTO, DESTINO,
    ERRO, BOTAO_TEXTO, BOTAO_BORDA, cor, misturar,
)
from .tipografia import escrever, quebrar_linhas
from .componentes import desenhar_tecla, largura_tecla
from .painel import desenhar_painel


def largura_painel(tela):
    return 420 if tela.get_width() >= 1100 else 340


def desenhar_tela_mundo(tela, fontes, desenho_grid, caminho, passo, pausado, agente_inicial, produto_inicial):
    tela.fill(FUNDO)
    largura, altura = tela.get_size()
    painel = pygame.Rect(largura - largura_painel(tela), 0, largura_painel(tela), altura)
    area_grid = pygame.Rect(0, 0, painel.x, altura)

    if caminho is None:
        desenho_grid.desenhar(tela, area_grid, agente=agente_inicial, produto=produto_inicial, produto_isolado=True)
    else:
        posicoes = [n.state.posicao_agente for n in caminho]
        estado = caminho[passo].state
        desenho_grid.desenhar(tela, area_grid, estado=estado, rastro=posicoes[:passo], plano=posicoes[passo + 1:],
                              agente=estado.posicao_agente, produto=estado.posicao_produto)
    desenhar_painel(tela, fontes, painel, caminho, passo, pausado)


def desenhar_fundo_quadriculado(tela):
    tela.fill(FUNDO)
    largura, altura = tela.get_size()
    linha = misturar(cor('#182028'), FUNDO, 0.5)
    for x in range(0, largura, 48):
        pygame.draw.line(tela, linha, (x, 0), (x, altura))
    for y in range(0, altura, 48):
        pygame.draw.line(tela, linha, (0, y), (largura, y))


def desenhar_tela_entrada(tela, fontes, texto_digitado, erro, tamanho_minimo, tamanho_maximo):
    # devolve os retângulos clicáveis: diminuir, aumentar e gerar
    desenhar_fundo_quadriculado(tela)
    largura_cartao = 520
    conteudo = pygame.Surface((largura_cartao, 900), pygame.SRCALPHA)
    x, largura = 44, largura_cartao - 88
    y = 44

    pygame.draw.circle(conteudo, DESTAQUE, (x + 7, y + 7), 7)
    pygame.draw.rect(conteudo, PRODUTO, pygame.Rect(x + 24, y + 1, 12, 12), border_radius=3)
    pygame.draw.circle(conteudo, DESTINO, (x + 53, y + 7), 7, 3)
    y += 28
    escrever(conteudo, fontes.roman(32, negrito=True), 'Entrega com A*', TEXTO, (x, y))
    y += 46
    for linha in quebrar_linhas(fontes.roman(16), 'O agente busca o produto e o entrega no destino pelo caminho de menor custo.', largura):
        escrever(conteudo, fontes.roman(16), linha, TEXTO_2, (x, y))
        y += 23
    y += 24

    escrever(conteudo, fontes.roman(13, negrito=True), 'DIMENSÃO DO GRID (N x N)', TEXTO_2, (x, y))
    y += 26
    diminuir = pygame.Rect(x, y, 56, 56)
    aumentar = pygame.Rect(x + largura - 56, y, 56, 56)
    campo = pygame.Rect(diminuir.right + 8, y, aumentar.x - diminuir.right - 16, 56)
    for botao, sinal in [(diminuir, '-'), (aumentar, '+')]:
        pygame.draw.rect(conteudo, CARTAO, botao, border_radius=10)
        pygame.draw.rect(conteudo, BOTAO_BORDA, botao, 1, border_radius=10)
        escrever(conteudo, fontes.roman(28), sinal, TEXTO, botao.center, 'center')
    pygame.draw.rect(conteudo, FUNDO, campo, border_radius=10)
    pygame.draw.rect(conteudo, ERRO if erro else DESTAQUE, campo, 2, border_radius=10)
    cursor = '_' if pygame.time.get_ticks() // 500 % 2 == 0 else ' '
    escrever(conteudo, fontes.mono(28), texto_digitado + cursor, TEXTO, campo.center, 'center')
    y += 66

    if erro:
        escrever(conteudo, fontes.roman(14), erro, ERRO, (x, y))
    else:
        escrever(conteudo, fontes.roman(14), f'Entre {tamanho_minimo} e {tamanho_maximo}', TEXTO_2, (x, y))
        if texto_digitado.isdigit():
            n = int(texto_digitado)
            escrever(conteudo, fontes.mono(13), f'{n * n} células', TEXTO_2, (x + largura, y + 1), 'topright')
    y += 46

    info = pygame.Rect(x, y, largura, 104)
    pygame.draw.rect(conteudo, CARTAO, info, border_radius=10)
    escrever(conteudo, fontes.roman(12, negrito=True), 'SORTEADO A CADA MUNDO', TEXTO_2, (x + 18, y + 16))
    escrever(conteudo, fontes.roman(15), 'Posição do agente, do produto e do destino', TEXTO_LEGENDA, (x + 18, y + 42))
    escrever(conteudo, fontes.roman(15), 'Quantidade e posição de obstáculos e pedágios', TEXTO_LEGENDA, (x + 18, y + 68))
    y += 104 + 28

    gerar = pygame.Rect(x, y, largura, 56)
    pygame.draw.rect(conteudo, DESTAQUE, gerar, border_radius=12)
    texto_botao = escrever(conteudo, fontes.roman(19, negrito=True), 'Gerar mundo', BOTAO_TEXTO, (gerar.centerx - 34, gerar.centery), 'center')
    fonte_chip = fontes.mono(12)
    chip = pygame.Rect(texto_botao.right + 12, 0, fonte_chip.size('ENTER')[0] + 16, 22)
    chip.centery = gerar.centery
    pygame.draw.rect(conteudo, misturar(BOTAO_TEXTO, DESTAQUE, 0.15), chip, border_radius=5)
    escrever(conteudo, fonte_chip, 'ENTER', BOTAO_TEXTO, chip.center, 'center')
    y += 56 + 28

    largura_rodape = largura_tecla(fontes, 'F11', 'tela cheia') + 20 + largura_tecla(fontes, 'ESC', 'sair')
    cursor_x = x + (largura - largura_rodape) // 2
    cursor_x += desenhar_tecla(conteudo, fontes, 'F11', 'tela cheia', (cursor_x, y)) + 20
    desenhar_tecla(conteudo, fontes, 'ESC', 'sair', (cursor_x, y))
    y += 22 + 36

    cartao = pygame.Rect(0, 0, largura_cartao, y)
    cartao.center = tela.get_rect().center
    sombra = pygame.Surface((cartao.w + 40, cartao.h + 40), pygame.SRCALPHA)
    pygame.draw.rect(sombra, (0, 0, 0, 70), sombra.get_rect().inflate(-20, -20).move(0, 12), border_radius=24)
    tela.blit(sombra, cartao.move(-20, -20))
    pygame.draw.rect(tela, PAINEL, cartao, border_radius=18)
    pygame.draw.rect(tela, BORDA, cartao, 1, border_radius=18)
    tela.blit(conteudo, cartao.topleft, pygame.Rect(0, 0, cartao.w, cartao.h))

    return {
        'diminuir': diminuir.move(cartao.topleft),
        'aumentar': aumentar.move(cartao.topleft),
        'gerar': gerar.move(cartao.topleft),
    }