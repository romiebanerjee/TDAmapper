# TDAmapper

Implementation of algorithm of Singh et.al.

https://research.math.osu.edu/tgda/mapperPBG.pdf

Input: Dataset in the form of a numpy array and a real valued continous function on the dataset

Output: Network graph representing topological summary

The script mapper.py takes as input a numpy array and lens parameters (see example below) and returns a json file mapperViz.json that contains the data of the mapper output simplicial complex (one-dimensional). The javascript file mapperViz.js interprets this json to produce the visualization. 

## Examples

### Iris dataset

```python
import mapper as mp
from sklearn.datasets import fetch_mldata
data = fetch_mldata('iris').data.tolist()
out = mp.Mapper(lens = "PCA", clusterer = "DBSCAN", n_rcover = [100, 3], clusterer_params  = (0.1,5))
out.write_to_json(data)
```
See the visualization [here](https://romiebanerjee.github.io/IRIS/index.html)


### Concentric Noisy Circles

```python
import mapper as mp
from sklearn import datasets
data, labels = datasets.make_circles(n_samples=2000, noise=0.03, factor=0.5)
X = data[:,0]
Y = data[:,1]
data = [[x,y] for x,y in zip(X,Y)]
out = mp.Mapper(lens = "PCA", clusterer = "DBSCAN", n_rcover = [50, 2], clusterer_params  = (0.1,5))
out.write_to_json(data)
```
See the visualization [here](https://romiebanerjee.github.io/CIRCLES/index.html)

### MNIST dataset

```python
import mapper as mp
from sklearn.datasets import fetch_mldata
mnist = fetch_mldata('MNIST original')
dataf = mnist.data[::70,:].astype(np.float32)

out = mp.Mapper(lens = "PCA", clusterer = "DBSCAN", n_rcover = [50, 2], clusterer_params  = (0.1,5))
out.write_to_json(data)
```
See the visualization [here](https://romiebanerjee.github.io/MNIST/index.html)





