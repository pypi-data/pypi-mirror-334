# Generalized Geography Game Solver

## Install

```console
$ pip install generalized-geography
```

## Example

```python
import generalized_geography as gg

graph = gg.UnlabeledMultiDiGraph()
graph.add_edges_from([(0,1), (0,1), (1,2), (2,3), (3,0), (1,2), (2,3), (0,2)])
node_type = gg.complete_classify(graph)
# node_type = {0: 'W', 1: 'L', 2: 'W', 3: 'L'}
```
