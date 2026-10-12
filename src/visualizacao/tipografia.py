"""Fontes (Latin Modern, a fonte do LaTeX) e funções de texto."""

import os

import pygame

PASTA_FONTES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fontes')


class Fontes:
    # Latin Modern (fonte do LaTeX), com fontes do sistema como reserva
    ARQUIVOS = {
        'roman': 'lmroman10-regular.otf',
        'roman_negrito': 'lmroman10-bold.otf',
        'mono': 'lmmono10-regular.otf',
    }
    RESERVA = {'roman': 'georgia', 'roman_negrito': 'georgia', 'mono': 'consolas'}

    def __init__(self):
        self.cache = {}

    def _carregar(self, tipo, tamanho):
        chave = (tipo, tamanho)
        if chave not in self.cache:
            caminho = os.path.join(PASTA_FONTES, self.ARQUIVOS[tipo])
            if os.path.exists(caminho):
                self.cache[chave] = pygame.font.Font(caminho, tamanho)
            else:
                self.cache[chave] = pygame.font.SysFont(self.RESERVA[tipo], tamanho, bold=tipo == 'roman_negrito')
        return self.cache[chave]

    def roman(self, tamanho, negrito=False):
        return self._carregar('roman_negrito' if negrito else 'roman', tamanho)

    def mono(self, tamanho):
        return self._carregar('mono', tamanho)


def escrever(tela, fonte, texto, cor_texto, posicao, ancora='topleft'):
    superficie = fonte.render(texto, True, cor_texto)
    retangulo = superficie.get_rect(**{ancora: posicao})
    tela.blit(superficie, retangulo)
    return retangulo


def quebrar_linhas(fonte, texto, largura):
    linhas, atual = [], ''
    for palavra in texto.split():
        tentativa = f'{atual} {palavra}'.strip()
        if fonte.size(tentativa)[0] <= largura:
            atual = tentativa
        else:
            linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas