from aigyminsper.search.graph import State


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class AgentSpecification(State):

    # Mundo compartilhado por todos os estados. O main.py substitui esses valores
    # por um mundo aleatório antes da busca; os valores abaixo são o exemplo da prova.
    LINHAS, COLUNAS = 10, 10
    DESTINO = (9,9)
    OBSTACULOS = {(0,3),(1,3),(2,3),(3,7),(3,8),(4,1),(4,2),(4,3),(6,6),(7,6),(8,6)}
    PEDAGIOS = {(0,1),(1,2),(2,4),(2,5),(4,8),(5,9),(6,3),(7,1)}

    def __init__(self, op, posicao_agente, posicao_produto, pegou_produto, entregou_produto, custo=1):
        super().__init__(op)
        self.posicao_agente = posicao_agente
        self.posicao_produto = posicao_produto
        self.pegou_produto = pegou_produto
        self.entregou_produto = entregou_produto
        self.custo = custo

    def successors(self):
        successors = []
        acoes = {
            "cima":(-1,0),"baixo":(1,0),
            "direita":(0,1), "esquerda":(0,-1),
            "pegar":None, "entregar":None
        }

        for acao, value in acoes.items():
            if acao == "pegar":
                if not self.pegou_produto and not self.entregou_produto and self.posicao_agente == self.posicao_produto:
                    successors.append(AgentSpecification(acao, self.posicao_agente, self.posicao_produto, True, self.entregou_produto))
            elif acao == "entregar":
                if self.pegou_produto and not self.entregou_produto and self.posicao_agente == self.DESTINO:
                    successors.append(AgentSpecification(acao, self.posicao_agente, self.posicao_produto, False, True))
            else:
                linha = self.posicao_agente[0] + value[0]
                coluna = self.posicao_agente[1] + value[1]
                nova_posicao = (linha, coluna)
                if 0 <= linha < self.LINHAS and 0 <= coluna < self.COLUNAS and nova_posicao not in self.OBSTACULOS:
                    custo = 1
                    if nova_posicao in self.PEDAGIOS:
                        custo += 2
                    posicao_produto = nova_posicao if self.pegou_produto else self.posicao_produto
                    successors.append(AgentSpecification(acao, nova_posicao, posicao_produto, self.pegou_produto, self.entregou_produto, custo))
        return successors

    def is_goal(self):
        return self.entregou_produto or (not self.pegou_produto and self.posicao_produto == self.DESTINO)

    def description(self):
        return "Agente que pega um produto e o entrega no destino em um grid com obstáculos e pedágios"

    def cost(self):
        return self.custo

    def h(self):
        if self.is_goal():
            return 0
        if not self.pegou_produto:
            return manhattan(self.posicao_agente, self.posicao_produto) + manhattan(self.posicao_produto, self.DESTINO)
        return manhattan(self.posicao_agente, self.DESTINO)

    def env(self):
        return f"{self.posicao_agente}#{self.posicao_produto}#{self.pegou_produto}#{self.entregou_produto}#{self.custo}"