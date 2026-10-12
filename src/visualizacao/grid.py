"""Desenho do grid: células, obstáculos, pedágios, rota, destino, agente e produto."""

import pygame

from AgentSpecification import AgentSpecification

from .cores import (
    FUNDO, BORDA, MOLDURA_GRID, LIVRE, OBSTACULO, OBSTACULO_SOMBRA, PEDAGIO_CLARO,
    PEDAGIO_ESCURO, PEDAGIO_BORDA, DESTAQUE, PRODUTO, PRODUTO_ESCURO, DESTINO, ERRO, misturar,
)


class DesenhoGrid:
    def __init__(self):
        self.cache_pedagio = {}
        self.cache_rastro = {}

    def geometria(self, area):
        n = AgentSpecification.LINHAS
        margem = max(16, min(48, min(area.w, area.h) // 16))
        lado_disponivel = min(area.w, area.h) - 2 * margem
        espaco = 4 if lado_disponivel // n >= 40 else (2 if lado_disponivel // n >= 16 else 1)
        celula = max(3, (lado_disponivel - 20 - espaco * (n - 1)) // n)
        lado = celula * n + espaco * (n - 1) + 20
        moldura = pygame.Rect(0, 0, lado, lado)
        moldura.center = area.center
        return moldura, celula, espaco

    def ladrilho_pedagio(self, tamanho, raio):
        chave = (tamanho, raio)
        if chave not in self.cache_pedagio:
            ladrilho = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
            ladrilho.fill(PEDAGIO_ESCURO)
            faixa = max(2, tamanho // 10)
            for x in range(-tamanho, 2 * tamanho, 2 * faixa):
                pygame.draw.polygon(ladrilho, PEDAGIO_CLARO,
                                    [(x, 0), (x + faixa, 0), (x + faixa - tamanho, tamanho), (x - tamanho, tamanho)])
            mascara = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
            pygame.draw.rect(mascara, (255, 255, 255, 255), mascara.get_rect(), border_radius=raio)
            ladrilho.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            pygame.draw.rect(ladrilho, PEDAGIO_BORDA, ladrilho.get_rect(), max(1, tamanho // 30), border_radius=raio)
            self.cache_pedagio[chave] = ladrilho
        return self.cache_pedagio[chave]

    def sobreposicao_rastro(self, tamanho, raio):
        chave = (tamanho, raio)
        if chave not in self.cache_rastro:
            camada = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
            pygame.draw.rect(camada, (*DESTAQUE, 26), camada.get_rect(), border_radius=raio)
            self.cache_rastro[chave] = camada
        return self.cache_rastro[chave]

    def desenhar(self, tela, area, estado=None, rastro=(), plano=(), agente=None, produto=None, produto_isolado=False):
        moldura, celula, espaco = self.geometria(area)
        pygame.draw.rect(tela, MOLDURA_GRID, moldura, border_radius=14)
        pygame.draw.rect(tela, BORDA, moldura, 1, border_radius=14)
        raio = max(1, celula // 12)

        def retangulo(posicao):
            linha, coluna = posicao
            return pygame.Rect(moldura.x + 10 + coluna * (celula + espaco),
                               moldura.y + 10 + linha * (celula + espaco), celula, celula)

        rastro = set(rastro)
        for linha in range(AgentSpecification.LINHAS):
            for coluna in range(AgentSpecification.COLUNAS):
                posicao = (linha, coluna)
                r = retangulo(posicao)
                if posicao in AgentSpecification.OBSTACULOS:
                    pygame.draw.rect(tela, OBSTACULO_SOMBRA, r, border_radius=raio)
                    pygame.draw.rect(tela, OBSTACULO, r.inflate(0, -max(1, celula // 20)).move(0, -max(1, celula // 40)),
                                     border_radius=raio)
                elif posicao in AgentSpecification.PEDAGIOS:
                    tela.blit(self.ladrilho_pedagio(celula, raio), r)
                else:
                    pygame.draw.rect(tela, LIVRE, r, border_radius=raio)
                if posicao in rastro:
                    tela.blit(self.sobreposicao_rastro(celula, raio), r)

        cor_ponto = misturar(DESTAQUE, LIVRE, 0.55)
        for posicao in plano:
            if posicao != AgentSpecification.DESTINO:
                pygame.draw.circle(tela, cor_ponto, retangulo(posicao).center, max(2, round(celula * 0.065)))

        # destino: alvo
        centro_destino = retangulo(AgentSpecification.DESTINO).center
        pygame.draw.circle(tela, DESTINO, centro_destino, max(4, round(celula * 0.28)), max(2, celula // 26))
        pygame.draw.circle(tela, DESTINO, centro_destino, max(2, round(celula * 0.09)))

        carregando = estado is not None and estado.pegou_produto
        entregue = estado is not None and estado.entregou_produto

        # agente antes do produto: quando os dois dividem a célula, o produto aparece por cima
        if agente is not None:
            centro = retangulo(agente).center
            raio_agente = max(3, round(celula * 0.30))
            anel = max(1, celula // 40)
            pygame.draw.circle(tela, DESTAQUE, centro, raio_agente + 3 * anel)
            pygame.draw.circle(tela, FUNDO, centro, raio_agente + 2 * anel)
            pygame.draw.circle(tela, DESTAQUE, centro, raio_agente)
            if carregando:
                lado = max(4, round(celula * 0.30))
                centro_caixa = (centro[0] + round(raio_agente * 0.8), centro[1] + round(raio_agente * 0.75))
                contorno = pygame.Rect(0, 0, lado + 4, lado + 4)
                contorno.center = centro_caixa
                pygame.draw.rect(tela, FUNDO, contorno, border_radius=max(2, lado // 5))
                self.caixa(tela, centro_caixa, lado, com_borda=False)

        if produto is not None and not carregando:
            r = retangulo(produto)
            if produto_isolado:
                self.borda_tracejada(tela, r.inflate(-max(2, celula // 10), -max(2, celula // 10)), ERRO, raio + 2)
            if entregue:
                # produto entregue: alvo e caixa por cima do agente
                pygame.draw.circle(tela, DESTINO, r.center, max(4, round(celula * 0.28)), max(2, celula // 26))
            tamanho = 0.32 if entregue else (0.4 if produto == agente else 0.48)
            self.caixa(tela, r.center, round(celula * tamanho))

    def caixa(self, tela, centro, lado, com_borda=True):
        caixa = pygame.Rect(0, 0, lado, lado)
        caixa.center = centro
        raio = max(2, lado // 6)
        pygame.draw.rect(tela, PRODUTO, caixa, border_radius=raio)
        fita = pygame.Rect(0, caixa.y, max(2, lado // 7), lado)
        fita.centerx = caixa.centerx
        pygame.draw.rect(tela, PRODUTO_ESCURO, fita)
        if com_borda:
            pygame.draw.rect(tela, PRODUTO_ESCURO, caixa, max(1, lado // 20), border_radius=raio)

    def borda_tracejada(self, tela, retangulo, cor_borda, raio):
        traco, vao, espessura = 6, 4, 2
        for inicio, fim in [(retangulo.topleft, retangulo.topright), (retangulo.topright, retangulo.bottomright),
                            (retangulo.bottomright, retangulo.bottomleft), (retangulo.bottomleft, retangulo.topleft)]:
            dx, dy = fim[0] - inicio[0], fim[1] - inicio[1]
            comprimento = max(abs(dx), abs(dy))
            passo_x, passo_y = (dx / comprimento, dy / comprimento) if comprimento else (0, 0)
            d = raio
            while d < comprimento - raio:
                a = (inicio[0] + passo_x * d, inicio[1] + passo_y * d)
                e = min(d + traco, comprimento - raio)
                b = (inicio[0] + passo_x * e, inicio[1] + passo_y * e)
                pygame.draw.line(tela, cor_borda, a, b, espessura)
                d += traco + vao
