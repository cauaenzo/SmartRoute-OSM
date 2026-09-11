# SmartRoute‑OSM
**Engenharia de Dados Espaciais & Análise Algorítmica** – Comparação de Dijkstra vs A* (heurística Haversine) na malha viária de **Quixadá – CE** (OSM)

---

## Descrição geral

Este repositório contém todo o pipeline para:

1. **Extrair** a rede viária de Quixadá a partir do OpenStreetMap usando **OSMnx**.
2. **Modelar** o grafo de ruas com **NetworkX** (sem utilizar APIs externas de roteamento).
3. **Implementar** do zero os algoritmos **Dijkstra** e **A\*** (heurística Haversine).
4. **Benchmark** de desempenho (distância, nós visitados, tempo de execução).
5. **Visualizar** resultados – rotas, isócronas, heatmaps de densidade – com **Folium** e **Seaborn/Matplotlib**.

> O foco está em demonstrar como processos de *ETL* espacial, modelagem de grafos e análise algorítmica podem ser integrados num workflow reproduzível e totalmente *open‑source*.

---

## Objetivos principais

| Nº | Objetivo |
|---|----------|
| 1 | **Modelagem de grafos** – Construir a rede viária a partir de dados OSM, gerar arquivos *graphml* e *CSV* para uso posterior. |
| 2 | **Implementação manual** – Codificar Dijkstra e A* sem recorrer a bibliotecas de roteamento prontas (ex.: `osmnx.shortest_path`). |
| 3 | **Benchmarking** – Medir distância total, número de nós explorados e tempo de execução (ms) para cada algoritmo. |
| 4 | **Visualização espacial** – Renderizar a rota, isócronas (5/10/15 min) e heatmap de densidade de nós em mapas interativos. |
| 5 | **Reprodutibilidade** – Notebook passo‑a‑passo, dependências declaradas e instruções claras de execução. |

---

## Tabela resumo do benchmark

| Algoritmo | Distância total (m) | Nós visitados | Tempo (ms) | Redução de exploração* |
|-----------|--------------------|--------------|-----------|------------------------|
| **Dijkstra** | 1 890,27 | 961 | 5,95 | – |
| **A* (Haversine)** | 1 890,27 | **81** | 4,94 | **91,57 %** menos nós explorados |

*% de redução calculada como \((\text{Nós Dijkstra} - \text{Nós A*}) / \text{Nós Dijkstra} \times 100\).*

---

## Estrutura do repositório

### Fluxo de execução

- **Extrair** dados OSM
- **Modelar** grafo (graphml)
- **Implementar** Dijkstra
- **Implementar** A* (Haversine)
- **Gerar métricas** Dijkstra
- **Gerar métricas** A*
- **Benchmark** comparativo
- **Visualizar** rotas e métricas
- **Isócronas & Heatmaps**

---

```
SmartRoute-OSM/
│
├─ routing/                  # Código reutilizável: algoritmos de roteamento
│   └─ algorithms.py         # Implementações Dijkstra e A* (Haversine)
│
├─ data/                     # Artefatos não versionados
│
└─ notebooks/
    ├─ 01_data_extraction_osm.ipynb
    ├─ 02_dijkstra_implementation.ipynb
    ├─ 03_astar_implementation.ipynb
    ├─ 04_benchmark_and_folium_map.ipynb
    └─ 05_spatial_analysis_extras.ipynb
```

---

## Tecnologias utilizadas

| Tecnologia | Uso |
|------------|-----|
| **Python ≥ 3.12** | Linguagem principal |
| **OSMnx** | Download e construção da malha viária |
| **NetworkX** | Estrutura de grafo e algoritmos base |
| **Pandas** | Manipulação de tabelas de métricas |
| **Folium** | Mapas interativos (Leaflet) |
| **Seaborn / Matplotlib** | Gráficos de barras (tempo, nós) |
| **Jupyter Notebook** | Ambiente de exploração e documentação |

---

## Passo a passo de instalação & execução

```bash
# Clone o repositório
git clone https://github.com/cauaenzo/SmartRoute-OSM.git
cd SmartRoute-OSM

# Crie e ative um virtualenv
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# Instale as dependências
pip install --upgrade pip
pip install -r requirements.txt   # (osmnx, pandas, folium, seaborn, matplotlib, jupyter)

# Inicie o Jupyter Notebook
jupyter notebook
```

Abra os notebooks em `notebooks/` **na ordem numérica** (`01_ → 05_`). Cada notebook contém explicações breves, código executável e comentários sobre como interpretar os resultados.

## Scripts e módulo de roteamento

Além dos notebooks, existe um módulo Python reutilizável em [routing/algorithms.py](C:/Users/cauae/Documents/SmartRoute-OSM/routing/algorithms.py) que contém implementações de Dijkstra e A* (heurística Haversine). Exemplos de uso:

- Carregar o grafo GraphML e usar as funções:

```python
import networkx as nx
from routing.algorithms import dijkstra, astar

G = nx.read_graphml('data/quixada_drive.graphml')  # caminho relativo ao repositório
start_node = ...   # id do nó de origem (int ou str conforme o graphml)
target_node = ...  # id do nó de destino

path, total_dist, nodes_visited = dijkstra(G, start_node, target_node)
# ou
path, total_dist, nodes_visited = astar(G, start_node, target_node)
```

- Exemplo rápido em linha de comando (Windows / cross-platform):

```bash
python -c "import networkx as nx; from routing.algorithms import dijkstra; G=nx.read_graphml('data/quixada_drive.graphml'); print(dijkstra(G, START, TARGET))"
```

Os resultados (rotas, métricas e mapas HTML) são gerados na pasta `data/` pelos notebooks; esses arquivos podem não estar versionados (veja `.gitignore`). Execute os notebooks na ordem para regenerar os artefatos.

---
## Referências

1. **Boeing, G. (2017).** *OSMnx: New methods for acquiring, constructing, analyzing, and visualizing complex street networks.* Computers, Environment and Urban Systems, 65, 126-139. https://doi.org/10.1016/j.compenvurbsys.2017.05.004
2. **Dijkstra, E. W. (1959).** *A note on two problems in connexion with graphs.* Numerische Mathematik, 1(1), 269–271.
3. **Hart, P. E., Nilsson, N. J., & Raphael, B. (1968).** *A Formal Basis for the Heuristic Determination of Minimum Cost Paths.* IEEE Transactions on Systems Science and Cybernetics, 4(2), 100–107.
4. **Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022).** *Introduction to Algorithms* (4th ed.). MIT Press.
5. **OpenStreetMap contributors.** *Planet dump.* (2026). Disponível em: https://www.openstreetmap.org.
---

## Licença

Distribuído sob a licença **MIT** – sinta‑se livre para usar, modificar e redistribuir o código, desde que mantenha o aviso de copyright.
