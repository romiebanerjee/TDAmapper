# TDAmapper

Implementation of algorithm of Singh et.al.

https://research.math.osu.edu/tgda/mapperPBG.pdf

Input: Dataset in the form of a numpy array and a real valued continous function on the dataset

Output: Network graph representing topological summary

The script mapper.py takes as input a numpy array and lens parameters (see example below) and returns a json file mapperViz.json that contains the data of the mapper output simplicial complex (one-dimensional). The javascript file mapperViz.js interprets this json to produce the visualization. 

Example: (Iris dataset)


```python
import mapper as mp

from sklearn.datasets import fetch_mldata
iris = fetch_mldata('iris')
data = iris.data.tolist()
out = mp.Mapper(lens = "PCA", clusterer = "DBSCAN", n_rcover = [100, 3], clusterer_params  = (0.1,5))
out.write_to_json(data)
```

Visualization: https://romiebanerjee.github.io/


