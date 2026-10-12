"""Peças pequenas reutilizadas pelas telas: chips de tecla, rótulos, status e cartões."""

import pygame

from .cores import BORDA, CARTAO, TEXTO, TEXTO_2, TEXTO_3, DESTAQUE, BOTAO_TEXTO, TECLA_SOMBRA
from .tipografia import escrever


def desenhar_tecla(tela, fontes, tecla, descricao, posicao, destaque=False):
    # chip de tecla seguido da descrição; devolve a largura total ocupada
    fonte_tecla = fontes.mono(12)
    largura_tecla = fonte_tecla.size(tecla)[0] + 14
    chip = pygame.Rect(posicao[0], posicao[1], largura_tecla, 22)
    if destaque:
        pygame.draw.rect(tela, DESTAQUE, chip, border_radius=5)
        escrever(tela, fonte_tecla, tecla, BOTAO_TEXTO, chip.center, 'center')
    else:
        pygame.draw.rect(tela, TECLA_SOMBRA, chip, border_radius=5)
        pygame.draw.rect(tela, BORDA, chip.inflate(0, -2).move(0, -1), border_radius=5)
        escrever(tela, fonte_tecla, tecla, TEXTO, chip.move(0, -1).center, 'center')
    largura = largura_tecla
    if descricao:
        rotulo = escrever(tela, fontes.roman(13), descricao, TEXTO_2, (chip.right + 7, chip.centery), 'midleft')
        largura = rotulo.right - chip.left
    return largura


def largura_tecla(fontes, tecla, descricao):
    largura = fontes.mono(12).size(tecla)[0] + 14
    if descricao:
        largura += 7 + fontes.roman(13).size(descricao)[0]
    return largura


def desenhar_teclas(tela, fontes, teclas, x, largura, y_base):
    # distribui os chips em linhas e alinha o bloco pela base; devolve o topo do bloco
    linhas, linha, ocupado = [], [], 0
    for tecla, descricao in teclas:
        w = largura_tecla(fontes, tecla, descricao)
        if linha and ocupado + 16 + w > largura:
            linhas.append(linha)
            linha, ocupado = [], 0
        ocupado += (16 if linha else 0) + w
        linha.append((tecla, descricao))
    if linha:
        linhas.append(linha)

    topo = y_base - len(linhas) * 30 + 8
    for i, linha in enumerate(linhas):
        cursor = x
        for tecla, descricao in linha:
            cursor += desenhar_tecla(tela, fontes, tecla, descricao, (cursor, topo + i * 30)) + 16
    return topo


def rotulo(tela, fontes, texto, posicao, cor_texto=TEXTO_2):
    return escrever(tela, fontes.roman(12, negrito=True), texto.upper(), cor_texto, posicao)


def chip_status(tela, fontes, texto, cor_texto, cor_fundo, direita, centro_y):
    fonte = fontes.roman(13, negrito=True)
    largura = fonte.size(texto)[0] + 40
    chip = pygame.Rect(0, 0, largura, 28)
    chip.midright = (direita, centro_y)
    pygame.draw.rect(tela, cor_fundo, chip, border_radius=14)
    pygame.draw.circle(tela, cor_texto, (chip.x + 16, chip.centery), 4)
    escrever(tela, fonte, texto, cor_texto, (chip.x + 26, chip.centery), 'midleft')


def cartao_valor(tela, fontes, retangulo, titulo, valor, sufixo='', cor_valor=TEXTO, mono=True):
    pygame.draw.rect(tela, CARTAO, retangulo, border_radius=10)
    rotulo(tela, fontes, titulo, (retangulo.x + 16, retangulo.y + 14))
    base = retangulo.y + 64
    if mono:
        r = escrever(tela, fontes.mono(28), valor, cor_valor, (retangulo.x + 16, base), 'bottomleft')
        if sufixo:
            escrever(tela, fontes.mono(18), sufixo, TEXTO_3, (r.right, base - 3), 'bottomleft')
    else:
        escrever(tela, fontes.roman(21, negrito=True), valor, cor_valor, (retangulo.x + 16, base - 2), 'bottomleft')