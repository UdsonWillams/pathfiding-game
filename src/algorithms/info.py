from dataclasses import dataclass
from typing import List


@dataclass
class AlgorithmInfo:
    key: str
    name: str
    algo_id: str
    badges: List[str]
    badges_colors: List[tuple]
    how_it_works: List[str]
    when_to_use: List[str]


ALGORITHM_INFO = {}

ALGORITHM_INFO["astar"] = AlgorithmInfo(
    key="astar",
    name="A* (A-Star)",
    algo_id="A*",
    badges=["Caminho otimo: sim", "Velocidade: rapida", "Terreno com peso: sim"],
    badges_colors=[(46, 204, 113), (46, 204, 113), (46, 204, 113)],
    how_it_works=[
        "O A* e uma mistura de duas ideias.",
        "Para cada celula ele calcula 3 valores:",
        "",
        "`g` = custo real ja gasto para chegar ate",
        "      aqui desde o start.",
        "      (ex: andou 3 celulas de grama => `g`=3,",
        "       pisou em lama que custa 5 => `g`=8)",
        "",
        "`h` = estimativa (heuristica) do custo que",
        "      ainda falta ate o goal. E um palpite",
        "      otimista, baseado na distancia Manhattan",
        "      (ignora paredes).",
        "",
        "`f` = `g` + `h` => o custo total previsto",
        "      da rota que passa por esta celula.",
        "",
        "O algoritmo sempre expande a celula com o",
        "MENOR `f`. Assim ele nao desperdica tempo",
        "indo na direcao errada (o `h` puxa para o",
        "goal) mas tambem nao se engana com atalhos",
        "falsos (o `g` mantem a conta real).",
    ],
    when_to_use=[
        "- Padrao para jogos em geral.",
        "- Caminho mais curto E rapido.",
        "- Funciona com ou sem terrenos de",
        "  custo diferente.",
    ],
)

ALGORITHM_INFO["dijkstra"] = AlgorithmInfo(
    key="dijkstra",
    name="Dijkstra",
    algo_id="Dijkstra",
    badges=["Caminho otimo: sim", "Velocidade: media", "Terreno com peso: sim"],
    badges_colors=[(46, 204, 113), (241, 196, 15), (46, 204, 113)],
    how_it_works=[
        "Pense no Dijkstra como o A* sem o palpite",
        "(`h` = 0). Ele so olha para o custo REAL",
        "ja gasto (o `g`) e sempre expande a celula",
        "com o menor `g` acumulado.",
        "",
        "Como nao tem heuristica guiando, ele expande",
        "em todas as direcoes igualmente - uma bola",
        "que cresce do start ate bater no goal.",
        "",
        "Por isso e mais lento que o A*, mas e",
        "garantido encontrar o caminho de menor custo,",
        "mesmo com terrenos ponderados.",
    ],
    when_to_use=[
        "- Quando voce nao tem uma boa heuristica.",
        "- Quando o custo das celulas varia muito",
        "  (mapas de jogo com terreno irregular).",
        "- E a base de algoritmos de roteamento",
        "  (ex: OSPF em redes).",
    ],
)

ALGORITHM_INFO["bfs"] = AlgorithmInfo(
    key="bfs",
    name="BFS (Busca em Largura)",
    algo_id="BFS",
    badges=["Caminho otimo: sim*", "Velocidade: media", "Peso: ignora"],
    badges_colors=[(46, 204, 113), (241, 196, 15), (231, 76, 60)],
    how_it_works=[
        "O BFS explora em camadas (ondas). Primeiro",
        "visita todas as celulas a 1 passo do start.",
        "Depois todas a 2 passos. Depois 3, 4...",
        "Ate achar o goal.",
        "",
        "Como cada passo custa o mesmo (ignora pesos),",
        "o primeiro caminho que chega ao goal e",
        "garantidamente o com menor NUMERO de celulas.",
        "",
        "E simples e correto, mas nao enxerga",
        "diferenca entre grama barata e lama cara -",
        "trata tudo igual.",
    ],
    when_to_use=[
        "- Grids sem terreno ponderado (tudo = 1).",
        "- Quando voce quer o menor numero de",
        "  passos, nao o menor custo.",
        "- Boa base para aprender busca.",
        "- Otimo apenas se todos os custos = 1.",
    ],
)

ALGORITHM_INFO["dfs"] = AlgorithmInfo(
    key="dfs",
    name="DFS (Busca em Profundidade)",
    algo_id="DFS",
    badges=["Caminho otimo: NAO", "Velocidade: rapida", "Peso: ignora"],
    badges_colors=[(231, 76, 60), (46, 204, 113), (231, 76, 60)],
    how_it_works=[
        "O DFS vai o mais fundo possivel antes de",
        "voltar. Ele escolhe um vizinho, depois um",
        "vizinho desse, e segue encostando na parede",
        "ate nao ter pra onde ir (beco sem saida).",
        "Ai ele volta (backtrack) para a ultima",
        "celula com alternativas e tenta outra",
        "direcao.",
        "",
        "Por isso ele ACHA um caminho, mas quase",
        "nunca e o melhor - pode dar uma volta",
        "enorme enquanto a saida estava ao lado.",
    ],
    when_to_use=[
        "- Para entender busca/backtracking.",
        "- Gerar labirintos (recursive backtracker).",
        "- NUNCA para pathfinding de gameplay.",
        "- Pode ficar preso em loops infinitos",
        "  se o grid tiver ciclos (aqui tratamos",
        "  marcando celulas ja visitadas).",
    ],
)

ALGORITHM_INFO["greedy"] = AlgorithmInfo(
    key="greedy",
    name="Greedy Best-First",
    algo_id="Greedy",
    badges=["Caminho otimo: NAO", "Velocidade: muito rapida", "Peso: ignora"],
    badges_colors=[(231, 76, 60), (46, 204, 113), (231, 76, 60)],
    how_it_works=[
        "O Greedy e o oposto do Dijkstra: ele ignora",
        "o custo ja gasto (`g`) e so olha a heuristica",
        "(`h`) - a estimativa de distancia ate o goal.",
        "",
        "Sempre expande a celula que PARECE estar mais",
        "perto do objetivo. E muito rapido porque voa",
        "na direcao do goal.",
        "",
        "Mas e facilmente enganado: se aparecer uma",
        "parede no meio do caminho, ele pode ficar",
        "preso ou fazer uma rota pessima, porque nao",
        "considera o quanto ja andou para chegar ali.",
    ],
    when_to_use=[
        "- Quando velocidade importa mais que",
        "  qualidade do caminho.",
        "- Mapas abertos, sem muitos obstaculos.",
        "- Como primeiro palpite antes de rodar",
        "  o A* completo.",
        "- Pode ser muito ruim em labirintos",
        "  complexos.",
    ],
)


def get_algorithm_info(algo_idx):
    keys = ["bfs", "dfs", "dijkstra", "astar", "greedy"]
    if 0 <= algo_idx < len(keys):
        return ALGORITHM_INFO.get(keys[algo_idx])
    return None
