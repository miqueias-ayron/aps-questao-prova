import random

from aigyminsper.search.search_algorithms import AEstrela

from AgentSpecification import AgentSpecification
import visualizacao

TAMANHO_MINIMO, TAMANHO_MAXIMO_GRID = 2, 50
PROPORCAO_MAXIMA_OBSTACULOS = 0.3
PROPORCAO_MAXIMA_PEDAGIOS = 0.15


def gerar_mundo(n):
    if not TAMANHO_MINIMO <= n <= TAMANHO_MAXIMO_GRID:
        raise ValueError(f"A dimensão do grid deve estar entre {TAMANHO_MINIMO} e {TAMANHO_MAXIMO_GRID}")

    celulas = [(linha, coluna) for linha in range(n) for coluna in range(n)]
    random.shuffle(celulas)

    # agente, produto e destino ficam em células distintas e livres
    agente, produto, destino = celulas[0], celulas[1], celulas[2]
    livres = celulas[3:]

    quantidade_obstaculos = random.randint(0, int(n * n * PROPORCAO_MAXIMA_OBSTACULOS))
    obstaculos = set(livres[:quantidade_obstaculos])
    livres = livres[quantidade_obstaculos:]

    quantidade_pedagios = random.randint(0, int(n * n * PROPORCAO_MAXIMA_PEDAGIOS))
    pedagios = set(livres[:quantidade_pedagios])

    AgentSpecification.LINHAS = AgentSpecification.COLUNAS = n
    AgentSpecification.DESTINO = destino
    AgentSpecification.OBSTACULOS = obstaculos
    AgentSpecification.PEDAGIOS = pedagios

    return agente, produto


def buscar(agente, produto):
    state = AgentSpecification('', agente, produto, False, False)
    algorithm = AEstrela()
    return algorithm.search(state, pruning='general')


def imprimir_resultado(result, agente, produto):
    print('Busca A*')
    print(f'Grid {AgentSpecification.LINHAS}x{AgentSpecification.COLUNAS} | agente {agente} | '
          f'produto {produto} | destino {AgentSpecification.DESTINO} | '
          f'{len(AgentSpecification.OBSTACULOS)} obstaculos | {len(AgentSpecification.PEDAGIOS)} pedagios')
    if result != None:
        print('Achou!')
        print(result.show_path())
        print('Custo:', result.g)
    else:
        print('Nao existe solucao para este problema')


def novo_mundo(n):
    agente, produto = gerar_mundo(n)
    resultado = buscar(agente, produto)
    imprimir_resultado(resultado, agente, produto)
    return resultado, agente, produto


def main():
    visualizacao.executar(novo_mundo, TAMANHO_MINIMO, TAMANHO_MAXIMO_GRID)


if __name__ == '__main__':
    main()