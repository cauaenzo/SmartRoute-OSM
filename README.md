# SmartRoute‑OSM

**Engenharia de Dados Espaciais & Análise Algorítmica** – Comparação de Dijkstra vs A* (heurística Haversine) na malha viária de **Quixadá – CE** (OSM)

---

## Research Question

> **Em que medida uma heurística geodésica (Haversine) reduz a complexidade computacional do algoritmo A* em relação ao Dijkstra clássico, mantendo a otimalidade do caminho, quando aplicados a redes viárias reais extraídas do OpenStreetMap?**

---

## Hypothesis

**H₁**: O algoritmo A* com heurística Haversine (distância euclidiana em esfera) visita significativamente menos nós que o Dijkstra, resultando em tempo de execução menor, sem comprometer a otimalidade do caminho (mesma distância total).

**H₀**: Não há diferença estatisticamente relevante no número de nós visitados nem no tempo de execução entre Dijkstra e A* (Haversine) na malha viária de Quixadá.

*Justificativa*: A heurística Haversine é admissível (nunca superestima o custo real em redes planas) e consistente, garantindo que A* expanda apenas nós promissores. Em grafos esparsos como redes viárias urbanas, espera-se redução drástica na fronteira de busca.

---

## Methodology

### 1. Aquisição e Preparação dos Dados (ETL Espacial)
- **Fonte**: OpenStreetMap via `OSMnx v2.1`
- **Área de estudo**: Quixadá, Ceará, Brazil (`place_name = "Quixadá, Ceará, Brazil"`)
- **Tipo de rede**: `drive` (vias dirigíveis)
- **Grafo resultante**: 3.647 nós, 9.762 arestas
- **Enriquecimento**: `ox.add_edge_speeds()` + `ox.add_edge_travel_times()` → atributos `speed_kph` e `travel_time` por aresta
- **Persistência**: GraphML (`data/quixada_drive.graphml`) para reprodutibilidade

### 2. Modelagem do Grafo
- **Estrutura**: `networkx.MultiDiGraph` (grafo direcionado com multi-arestas)
- **Peso padrão**: `length` (metros, geodésico)
- **Nós**: IDs inteiros OSM; atributos `x` (lon), `y` (lat)
- **Arestas**: `length`, `speed_kph`, `travel_time`, `highway`, `geometry`

### 3. Implementação dos Algoritmos (from scratch)
Local: `routing/algorithms.py`

| Algoritmo | Estratégia | Heurística | Complexidade Teórica |
|-----------|------------|------------|---------------------|
| **Dijkstra** | Busca uniforme (g(n)) | — | O((V+E) log V) |
| **A*** | Busca guiada (f(n) = g(n) + h(n)) | Haversine (admissível) | O((V+E) log V) worst-case; na prática ≪ Dijkstra |

**Detalhes da implementação**:
- `heapq` para fila de prioridade (min-heap)
- `@lru_cache` na heurística para evitar recálculos em A*
- Retorno: `(path: list[int], total_cost: float, nodes_visited: int)`
- Funções expostas: `dijkstra()`, `astar()`, `haversine_heuristic()`

### 4. Protocolo Experimental
- **Par origem-destino fixo**: nó 0 → nó N-1 (primeiro e último do grafo)
- **Métricas coletadas**: distância total (m), nós visitados, tempo execução (ms)
- **Execução única** (determinística; sem variação estocástica)
- **Ambiente**: Python 3.14, Jupyter Notebook, dependências em `requirements.txt`

### 5. Análise Espacial Complementar
- **Isócronas** (5, 10, 15 min) via convex hull de nós alcançáveis (velocidade média 5 m/s)
- **Heatmap de densidade viária** (Folium HeatMap)
- **Mapa de rota interativo** (Folium PolyLine + markers)

---

## Experiments

### Pipeline de Execução (ordem obrigatória)

| Etapa | Notebook | Artefatos Gerados |
|-------|----------|-------------------|
| 1. Extração OSM | `notebooks/01_data_extraction_osm.ipynb` | `data/quixada_drive.graphml` |
| 2. Dijkstra | `notebooks/02_dijkstra_implementation.ipynb` | `data/dijkstra_path.json`, `data/dijkstra_metrics.csv` |
| 3. A* (Haversine) | `notebooks/03_astar_implementation.ipynb` | `data/astar_path.json`, `data/astar_metrics.csv` |
| 4. Benchmark + Mapa | `notebooks/04_benchmark_and_folium_map.ipynb` | `data/route_map.html`, tabela comparativa |
| 5. Análise Espacial | `notebooks/05_spatial_analysis_extras.ipynb` | `data/spatial_analysis_map.html`, `data/spatial_analysis_heatmap.html` |

### Configuração do Experimento
- **Hardware**: CPU não especificado (execução em notebook local)
- **Software**: versões fixadas em `requirements.txt`
- **Semente/Estado**: determinístico (sem aleatoriedade)

---

## Results

### Benchmark Comparativo (Única execução, origem→destino fixos)

| Métrica | Dijkstra | A* (Haversine) | Ganho A* |
|---------|----------|----------------|----------|
| **Distância total (m)** | 1.890,27 | 1.890,27 | 0% (ótimo igual) |
| **Nós visitados** | 961 | **81** | **−91,57%** |
| **Tempo execução (ms)** | 5,95 | **4,94** | **−17%** |

### Interpretação
- **Optimalidade preservada**: Ambos encontram caminho idêntico (1.890,27 m)
- **Eficiência de exploração**: A* visita **11,9× menos nós** (81 vs 961)
- **Speedup modesto em tempo**: Overhead da heurística (cálculo Haversine + cache) compensa parcialmente o ganho de nós
- **Conclusão**: H₁ **confirmada** – heurística Haversine reduz drasticamente a fronteira de busca mantendo otimalidade

### Visualizações Geradas
- `data/route_map.html` – rota ótima sobre OSM (Folium)
- `data/spatial_analysis_map.html` – isócronas 5/10/15 min + malha viária
- `data/spatial_analysis_heatmap.html` – densidade de nós (HeatMap)

---

## Limitations

1. **Amostra única (n=1)**: Apenas um par origem-destino testado; resultados podem variar com topologia, distância e densidade da rede
2. **Ausência de significância estatística**: Sem execuções repetidas, intervalos de confiança ou testes de hipótese (t-test, Wilcoxon)
3. **Heurística estática**: Haversine assume velocidade constante; não considera tráfego, restrições de sentido, tempo real
4. **Grafo estático**: Não modela dinâmica temporal (horários de pico, interdições)
5. **Escala municipal**: Quixadá (~3,6k nós); comportamento em metrópoles (São Paulo ~1M nós) pode diferir
6. **Implementação educacional**: Não otimizada para produção (ex.: sem contraction hierarchies, landmarks, ou ALT)
7. **Métrica de tempo**: `time.perf_counter()` em notebook – sujeito a ruído de GC, JIT, outros processos

---

## Future Work

### Curto Prazo (Incremental)
- [ ] Benchmark sistemático: 100+ pares OD aleatórios + testes estatísticos (IC 95%, p-value)
- [ ] Comparar heurísticas: Haversine vs. Euclidiana (projetada) vs. Octile vs. Landmark-based (ALT)
- [ ] Implementar **bidirectional A*** e **Contraction Hierarchies** (CH) para speedup real
- [ ] Perfil de memória (tracemalloc) e cache-misses (perf)

### Médio Prazo (Extensão)
- [ ] Integração com **OSRM** / **Valhalla** como baseline industrial
- [ ] Dados de tráfego real (TomTom, HERE, ou aberto: Uber Movement) → heurística dinâmica
- [ ] Multi-objetivo: tempo + distância + elevação + segurança
- [ ] Generalização para multi-modal (walk + bike + transit)

### Longo Prazo (Pesquisa)
- [ ] **Learning-based heuristics**: GNN para prever h(n) treinada em subgrafos
- [ ] **Dynamic graphs**: Atualização incremental de edge weights (traffic incidents)
- [ ] **Robust routing**: Pareto-frontier sob incerteza (stochastic travel times)
- [ ] Publicação: artigo em conferência (SBRC, GeoInfo, SIGSPATIAL) ou journal (Computers & Geosciences)

---

## Repository Structure

```
SmartRoute-OSM/
│
├── README.md                 # Este arquivo
├── requirements.txt          # Dependências fixadas (pip freeze)
├── LICENSE                   # MIT
├── .gitignore
│
├── routing/                  # Código reutilizável (módulo Python)
│   ├── __init__.py
│   └── algorithms.py         # Dijkstra, A*, Haversine
│
├── data/                     # Artefatos (não versionados; .gitignore)
│   ├── quixada_drive.graphml
│   ├── dijkstra_path.json / _metrics.csv
│   ├── astar_path.json / _metrics.csv
│   ├── route_map.html
│   ├── spatial_analysis_map.html
│   └── spatial_analysis_heatmap.html
│
├── notebooks/                # Pipeline executável (ordem numérica)
│   ├── 01_data_extraction_osm.ipynb
│   ├── 02_dijkstra_implementation.ipynb
│   ├── 03_astar_implementation.ipynb
│   ├── 04_benchmark_and_folium_map.ipynb
│   └── 05_spatial_analysis_extras.ipynb
│
└── figures/                  # (Opcional) Exportação estática para paper
    ├── benchmark_bars.png
    ├── route_map.png
    └── isochrones.png
```

---

## Quick Start

```bash
# Clone o repositório
git clone https://github.com/cauaenzo/SmartRoute-OSM.git
cd SmartRoute-OSM

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

jupyter notebook
# Abra notebooks/01_data_extraction_osm.ipynb → execute em ordem
```

---

## Referências Bibliográficas

### Fundamentos Algorítmicos
1. **Dijkstra, E. W. (1959).** *A note on two problems in connexion with graphs.* Numerische Mathematik, 1(1), 269–271. https://doi.org/10.1007/BF01386390
2. **Hart, P. E., Nilsson, N. J., & Raphael, B. (1968).** *A Formal Basis for the Heuristic Determination of Minimum Cost Paths.* IEEE Transactions on Systems Science and Cybernetics, 4(2), 100–107. https://doi.org/10.1109/TSSC.1968.300136
3. **Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022).** *Introduction to Algorithms* (4th ed.). MIT Press. Cap. 24 (Single-Source Shortest Paths) e 25 (All-Pairs).
4. **Russell, S., & Norvig, P. (2021).** *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson. Cap. 3 (Search) e 4 (Heuristic Search).

### Heurísticas Geodésicas e A* em Redes Viárias
5. **Goldberg, A. V., & Harrelson, C. (2005).** *Computing the Shortest Path: A* Search Meets Graph Theory.* Proc. SODA, 156–165. (Introduz ALT – A*, Landmarks, Triangle Inequality)
6. **Bast, H., Delling, D., Goldberg, A., Müller-Hannemann, M., Pajor, T., Sanders, P., Wagner, D., & Werneck, R. F. (2016).** *Route Planning in Transportation Networks.* In: Algorithm Engineering (pp. 19–80). Springer. https://arxiv.org/abs/1504.05140
7. **Geisberger, R., Sanders, P., Schultes, D., & Delling, D. (2008).** *Contraction Hierarchies: Faster and Simpler Hierarchical Routing in Road Networks.* WEA, 319–333.
8. **Delling, D., & Werneck, R. F. (2013).** *Faster Customizable Routing.* Proc. SEA, 30–42.

### OSMnx, Dados Abertos e Análise Espacial
9. **Boeing, G. (2017).** *OSMnx: New methods for acquiring, constructing, analyzing, and visualizing complex street networks.* Computers, Environment and Urban Systems, 65, 126–139. https://doi.org/10.1016/j.compenvurbsys.2017.05.004
10. **Boeing, G. (2020).** *A multi-scale analysis of 27,000 urban street networks: Every US city, town, and urbanized area.* Environment and Planning B: Urban Analytics and City Science, 48(4), 1–18. https://doi.org/10.1177/2399808320972353

Resolving conflicts between develop and main and committing changes  develop
1 conflicting file11. **OpenStreetMap Contributors. (2026).** *Planet dump.* https://planet.openstreetmap.org
12. **Haklay, M., & Weber, P. (2008).** *OpenStreetMap: User-Generated Street Maps.* IEEE Pervasive Computing, 7(4), 12–18.

### Visualização e Análise Espacial em Python
13. **Rey, S. J., & Anselin, L. (2010).** *PySAL: A Python Library of Spatial Analytical Methods.* In: Handbook of Applied Spatial Analysis. Springer.
14. **Jordahl, K., et al. (2024).** *GeoPandas: Python tools for geographic data.* https://geopandas.org
15. **Folium Contributors. (2024).** *Folium: Python Data. Leaflet.js Maps.* https://python-visualization.github.io/folium

### Benchmarking e Metodologia Experimental
16. **Johnson, D. S. (2002).** *A Theoretician's Guide to the Experimental Analysis of Algorithms.* In: Data Structures, Near Neighbor Searches, and Methodology (pp. 215–250). AMS.
17. **McGeoch, C. C. (2012).** *A Guide to Experimental Algorithmics.* Cambridge University Press.
18. **Morin, P. (2023).** *Experimental Algorithmics: A Tutorial.* https://arxiv.org/abs/2301.08245

---

## Licença

Distribuído sob a licença **MIT** – sinta‑se livre para usar, modificar e redistribuir o código, desde que mantenha o aviso de copyright.
