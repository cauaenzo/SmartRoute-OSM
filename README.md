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

*% de redução calculada como \((\text{Nós Dijkstra} - \text{Nós A*}) / \text{Nós Dijkstra} \times 100\).

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
├─ data/                     # Arquivos gerados / estáticos
│   ├─ quixada_drive.graphml  # Grafo viário (OSMnx)
│   ├─ dijkstra_metrics.csv   # Métricas Dijkstra
│   ├─ astar_metrics.csv      # Métricas A*
│   ├─ dijkstra_visited_nodes.json
│   ├─ astar_visited_nodes.json
│   └─ astar_path.json        # Lista de nós da rota ótima
│
└─ notebooks/
    ├─ 01_data_extraction_osm.ipynb          # Baixa OSM, cria graphml
    ├─ 02_dijkstra_implementation.ipynb     # Algoritmo Dijkstra + métricas
    ├─ 03_astar_implementation.ipynb        # Algoritmo A* (Haversine) + métricas
    ├─ 04_benchmark_and_folium_map.ipynb    # Tabela comparativa + gráficos + visualização da rota
    └─ 05_spatial_analysis_extras.ipynb    # Isócronas, heatmap e visualizações avançadas
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
