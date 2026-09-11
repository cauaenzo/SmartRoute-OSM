import heapq
import math
from functools import lru_cache
from typing import Callable, Optional


def dijkstra(
    graph,
    start_node: int,
    target_node: int,
    weight_attribute: str = "length",
) -> tuple[list[int], float, int]:
    """
    Calcula o menor caminho usando o algoritmo de Dijkstra.

    Returns:
        path: Lista de nós representando o caminho.
        total_cost: Distância/peso total percorrido.
        nodes_visited: Quantidade de nós explorados durante a busca.

    Considerações: ainda em desenvolvimento. algorítimo provisório.
    """
    distances = {node: float("inf") for node in graph.nodes}
    distances[start_node] = 0
    predecessors = {node: None for node in graph.nodes}

    priority_queue = [(0, start_node)]
    nodes_visited = 0

    while priority_queue:
        current_dist, current_node = heapq.heappop(priority_queue)
        nodes_visited += 1

        if current_node == target_node:
            break

        if current_dist > distances[current_node]:
            continue

        for neighbor in graph.neighbors(current_node):
            edge_data = graph.get_edge_data(current_node, neighbor)[0]
            edge_weight = float(edge_data.get(weight_attribute, 1))

            distance = current_dist + edge_weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    path = []
    curr = target_node
    while curr is not None:
        path.append(curr)
        curr = predecessors[curr]
    path.reverse()

    return path, distances[target_node], nodes_visited


def haversine_heuristic(node_a: int, node_b: int, graph) -> float:
    """Calcula a distância em metros em linha reta entre dois nós (Haversine)."""
    y1, x1 = float(graph.nodes[node_a]["y"]), float(graph.nodes[node_a]["x"])
    y2, x2 = float(graph.nodes[node_b]["y"]), float(graph.nodes[node_b]["x"])

    R = 6371000
    phi1, phi2 = math.radians(y1), math.radians(y2)
    dphi = math.radians(y2 - y1)
    dlambda = math.radians(x2 - x1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def astar(
    graph,
    start_node: int,
    target_node: int,
    weight_attribute: str = "length",
    heuristic: Optional[Callable[[int, int, object], float]] = None,
) -> tuple[list[int], float, int]:
    """
    Calcula o menor caminho usando o algoritmo A*.

    Args:
        graph: Grafo NetworkX.
        start_node: Nó de origem.
        target_node: Nó de destino.
        weight_attribute: Atributo da aresta a ser usado como peso.
        heuristic: Função heurística h(n). Default: haversine_heuristic.

    Returns:
        path: Lista de nós representando o caminho.
        total_cost: Custo total (g_score do target).
        nodes_visited: Quantidade de nós explorados.
    """
    if heuristic is None:
        heuristic = haversine_heuristic

    @lru_cache(maxsize=None)
    def cached_heuristic(node):
        return heuristic(node, target_node, graph)

    g_score = {node: float("inf") for node in graph.nodes}
    g_score[start_node] = 0

    f_score = {node: float("inf") for node in graph.nodes}
    f_score[start_node] = cached_heuristic(start_node)

    predecessors = {node: None for node in graph.nodes}
    priority_queue = [(f_score[start_node], start_node)]
    nodes_visited = 0

    while priority_queue:
        _, current_node = heapq.heappop(priority_queue)
        nodes_visited += 1

        if current_node == target_node:
            break

        for neighbor in graph.neighbors(current_node):
            edge_data = graph.get_edge_data(current_node, neighbor)[0]
            edge_weight = float(edge_data.get(weight_attribute, 1))

            tentative_g = g_score[current_node] + edge_weight

            if tentative_g < g_score[neighbor]:
                predecessors[neighbor] = current_node
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + cached_heuristic(neighbor)
                heapq.heappush(priority_queue, (f_score[neighbor], neighbor))

    path = []
    curr = target_node
    while curr is not None:
        path.append(curr)
        curr = predecessors[curr]
    path.reverse()

    return path, g_score[target_node], nodes_visited


def dijkstra_routing(graph, start_node: int, target_node: int, weight_attribute: str = "length") -> tuple[list[int], float, int]:
    return dijkstra(graph, start_node, target_node, weight_attribute)


def astar_routing(graph, start_node: int, target_node: int, weight_attribute: str = "length") -> tuple[list[int], float, int]:
    return astar(graph, start_node, target_node, weight_attribute)