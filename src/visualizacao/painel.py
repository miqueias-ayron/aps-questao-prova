"""Painel lateral da tela do grid: andamento da busca ou aviso de sem solução."""

import pygame

from AgentSpecification import AgentSpecification

from .cores import (
    PAINEL, BORDA, CARTAO, OBSTACULO, PEDAGIO_ESCURO, PEDAGIO_BORDA, TEXTO, TEXTO_2, TEXTO_3,
    TEXTO_LEGENDA, DESTAQUE, DESTAQUE_TEXTO, DESTAQUE_FUNDO, PRODUTO, PRODUTO_TEXTO, DESTINO,
    ERRO, ERRO_FUNDO, ALERTA_FUNDO, ALERTA_BORDA, ALERTA_TITULO, ALERTA_TEXTO, SUCESSO,
    SUCESSO_FUNDO, misturar,
)
from .tipografia import escrever, quebrar_linhas
from .componentes import desenhar_tecla, desenhar_teclas, rotulo, chip_status, cartao_valor


def desenhar_painel(tela, fontes, painel, caminho, passo, pausado):
    pygame.draw.rect(tela, PAINEL, painel)
    pygame.draw.line(tela, BORDA, painel.topleft, painel.bottomleft)
    x = painel.x + 36
    largura = painel.w - 72
    direita = x + largura

    # cabecalho
    escrever(tela, fontes.roman(26, negrito=True), 'Entrega com A*', TEXTO, (x, painel.y + 54), 'midleft')
    if caminho is None:
        chip_status(tela, fontes, 'Sem solução', ERRO, ERRO_FUNDO, direita, painel.y + 54)
    elif passo == len(caminho) - 1:
        chip_status(tela, fontes, 'Concluído', SUCESSO, SUCESSO_FUNDO, direita, painel.y + 54)
    elif pausado:
        chip_status(tela, fontes, 'Pausado', TEXTO_2, CARTAO, direita, painel.y + 54)
    else:
        chip_status(tela, fontes, 'Executando', DESTAQUE_TEXTO, DESTAQUE_FUNDO, direita, painel.y + 54)
    n = AgentSpecification.LINHAS
    info = f'Grid {n}×{n} · {len(AgentSpecification.OBSTACULOS)} obstáculos · {len(AgentSpecification.PEDAGIOS)} pedágios'
    escrever(tela, fontes.mono(13), info, TEXTO_2, (x, painel.y + 80))
    y = painel.y + 122

    # rodape: teclas e legenda, de baixo para cima
    if caminho is None:
        teclas = [('F11', 'tela cheia'), ('ESC', 'sair')]
    else:
        teclas = [('ESPAÇO', 'pausar'), ('R', 'reiniciar'), ('N', 'novo mundo'),
                  ('D', 'dimensão'), ('F11', 'tela cheia'), ('ESC', 'sair')]
    topo_teclas = desenhar_teclas(tela, fontes, teclas, x, largura, painel.bottom - 36)
    pygame.draw.line(tela, BORDA, (x, topo_teclas - 20), (direita, topo_teclas - 20))
    limite = topo_teclas - 20

    if caminho is not None:
        limite = desenhar_legenda(tela, fontes, x, largura, limite - 28) - 24
        desenhar_andamento(tela, fontes, x, largura, y, limite, caminho, passo)
    else:
        desenhar_sem_solucao(tela, fontes, x, largura, y)


def desenhar_legenda(tela, fontes, x, largura, base):
    itens = ['agente', 'produto', 'destino', 'obstaculo', 'pedagio', 'rota']
    nomes = {'agente': 'Agente', 'produto': 'Produto', 'destino': 'Destino', 'obstaculo': 'Obstáculo',
             'pedagio': 'Pedágio (+2)', 'rota': 'Rota planejada'}
    altura_linha = 28
    topo = base - 3 * altura_linha
    coluna = largura // 2
    for i, item in enumerate(itens):
        cx = x + (i % 2) * coluna + 9
        cy = topo + (i // 2) * altura_linha + 9
        if item == 'agente':
            pygame.draw.circle(tela, DESTAQUE, (cx, cy), 9)
        elif item == 'produto':
            pygame.draw.rect(tela, PRODUTO, pygame.Rect(cx - 8, cy - 8, 16, 16), border_radius=4)
        elif item == 'destino':
            pygame.draw.circle(tela, DESTINO, (cx, cy), 9, 3)
        elif item == 'obstaculo':
            pygame.draw.rect(tela, OBSTACULO, pygame.Rect(cx - 9, cy - 9, 18, 18), border_radius=4)
        elif item == 'pedagio':
            pygame.draw.rect(tela, PEDAGIO_ESCURO, pygame.Rect(cx - 9, cy - 9, 18, 18), border_radius=4)
            pygame.draw.rect(tela, PEDAGIO_BORDA, pygame.Rect(cx - 9, cy - 9, 18, 18), 2, border_radius=4)
        else:
            pygame.draw.circle(tela, misturar(DESTAQUE, PAINEL, 0.55), (cx, cy), 4)
        escrever(tela, fontes.roman(14), nomes[item], TEXTO_LEGENDA, (cx + 19, cy), 'midleft')
    return topo


def desenhar_andamento(tela, fontes, x, largura, y, limite, caminho, passo):
    nodo = caminho[passo]
    estado = nodo.state
    total = len(caminho) - 1

    # cartoes
    meia = (largura - 12) // 2
    cartao_valor(tela, fontes, pygame.Rect(x, y, meia, 78), 'Passo', str(passo), f' / {total}')
    cartao_valor(tela, fontes, pygame.Rect(x + meia + 12, y, meia, 78), 'Custo', str(nodo.g), f' / {caminho[-1].g}')
    acao = estado.operator or 'início'
    cartao_valor(tela, fontes, pygame.Rect(x, y + 90, meia, 78), 'Ação', acao, mono=False)
    if estado.entregou_produto:
        produto, cor_produto = 'Entregue', SUCESSO
    elif estado.pegou_produto:
        produto, cor_produto = 'Carregando', PRODUTO_TEXTO
    else:
        produto, cor_produto = 'Aguardando', TEXTO_2
    cartao_valor(tela, fontes, pygame.Rect(x + meia + 12, y + 90, meia, 78), 'Produto', produto, cor_valor=cor_produto, mono=False)
    y += 196

    # progresso, com a marca do momento em que o produto é pego
    barra = pygame.Rect(x, y, largura, 6)
    pygame.draw.rect(tela, BORDA, barra, border_radius=3)
    if total:
        preenchido = barra.copy()
        preenchido.w = round(largura * passo / total)
        if preenchido.w:
            pygame.draw.rect(tela, DESTAQUE, preenchido, border_radius=3)
        indice_pegar = next((i for i, n in enumerate(caminho) if n.state.operator == 'pegar'), None)
        if indice_pegar is not None:
            marca_x = x + round(largura * indice_pegar / total)
            pygame.draw.rect(tela, PRODUTO, pygame.Rect(marca_x - 2, y - 4, 4, 14), border_radius=2)
            escrever(tela, fontes.roman(13), 'pegar', TEXTO_2, (min(marca_x, x + largura - 120), y + 14), 'midtop')
    escrever(tela, fontes.roman(13), 'entregar', TEXTO_2, (x + largura, y + 14), 'topright')
    y += 52

    # últimas acoes
    rotulo(tela, fontes, 'Últimas ações', (x, y))
    y += 28
    linhas_cabem = max(0, (limite - y) // 26)
    inicio = max(1, passo - linhas_cabem + 1)
    for i in range(passo, inicio - 1, -1):
        nodo_i = caminho[i]
        operador = nodo_i.state.operator
        if operador in ('pegar', 'entregar'):
            cor_linha = PRODUTO_TEXTO
        elif i == passo:
            cor_linha = TEXTO
        else:
            cor_linha = TEXTO_2
        fonte = fontes.mono(14)
        escrever(tela, fonte, str(i), TEXTO_3, (x, y))
        escrever(tela, fonte, operador, cor_linha, (x + 40, y))
        delta = nodo_i.g - caminho[i - 1].g
        escrever(tela, fonte, f'+{delta} → {nodo_i.g}', TEXTO_2, (x + largura, y), 'topright')
        y += 26


def desenhar_sem_solucao(tela, fontes, x, largura, y):
    # alerta
    texto = ('O A* explorou todos os estados alcançáveis a partir do agente e nenhum deles '
             'chega à meta. Obstáculos bloqueiam o caminho.')
    linhas = quebrar_linhas(fontes.roman(15), texto, largura - 40)
    alerta = pygame.Rect(x, y, largura, 20 + 26 + 10 + len(linhas) * 22 + 20)
    pygame.draw.rect(tela, ALERTA_FUNDO, alerta, border_radius=12)
    pygame.draw.rect(tela, ALERTA_BORDA, alerta, 1, border_radius=12)
    escrever(tela, fontes.roman(19, negrito=True), 'Não existe solução', ALERTA_TITULO, (x + 20, y + 20))
    for i, linha in enumerate(linhas):
        escrever(tela, fontes.roman(15), linha, ALERTA_TEXTO, (x + 20, y + 56 + i * 22))
    y = alerta.bottom + 28

    meia = (largura - 12) // 2
    cartao_valor(tela, fontes, pygame.Rect(x, y, meia, 78), 'Passos', '—', cor_valor=TEXTO_3)
    cartao_valor(tela, fontes, pygame.Rect(x + meia + 12, y, meia, 78), 'Custo', '—', cor_valor=TEXTO_3)
    y += 106

    rotulo(tela, fontes, 'O que fazer', (x, y))
    y += 28
    for tecla, texto_opcao, destaque in [('N', 'Gerar outro mundo do mesmo tamanho', True),
                                         ('D', 'Escolher outra dimensão', False)]:
        linha = pygame.Rect(x, y, largura, 50)
        pygame.draw.rect(tela, DESTAQUE_FUNDO if destaque else CARTAO, linha, border_radius=10)
        desenhar_tecla(tela, fontes, tecla, '', (x + 16, linha.centery - 11), destaque=destaque)
        escrever(tela, fontes.roman(16), texto_opcao, TEXTO if destaque else TEXTO_LEGENDA, (x + 52, linha.centery), 'midleft')
        y += 60