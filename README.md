# TDAmapper

Implementation of algorithm of Singh et.al.

https://research.math.osu.edu/tgda/mapperPBG.pdf

Input: Dataset in the form of a numpy array and a real valued continous function on the dataset

Output: Network graph representing topological summary

Sample compute: (Iris dataset)


```python
import mapper as mp
```


```python
from sklearn.datasets import fetch_mldata
iris = fetch_mldata('iris')
data = iris.data.tolist()
```


```python
out = mp.Mapper(lens = "PCA", clusterer = "DBSCAN", n_rcover = [100, 3], clusterer_params  = (0.1,5))
out.write_to_json(data)
```

Visualization: https://romiebanerjee.github.io/


