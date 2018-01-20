#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 06:56:05 2017

@author: romie
"""

import numpy as np
import pandas as pd
import json 

def flatten(A):
        if A == []: return A
        if type(A[0]) == list:
            return flatten(A[0]) + flatten(A[1:])
        else: return [A[0]] + flatten(A[1:])

class Lens():
    def __init__(self, name):
        self.name = name

    def fit_project(self,data):

        if self.name == "PCA":
            frame = pd.DataFrame({"data_points":data})
            from sklearn.decomposition import PCA
            pca = PCA(n_components = 1)
            frame["projected"] = pca.fit_transform(data) 
            return frame
            
        elif self.name == "eccentricity":
            frame = pd.DataFrame({"data_points": data})
            from sklearn.metrics.pairwise import euclidean_distances
            projected =  np.array([np.average(euclidean_distances(data,[x])) for x in data])
            frame["projected"] = projected
            return frame
              
        elif self.name == "Gauss_density":
            frame = pd.DataFrame({"data_points":data})
            from sklearn.metrics.pairwise import rbf_kernel
            projected = np.array([np.average(rbf_kernel(data, [x])) for x in data])
            frame["projected"] = projected
            return frame

        else: pass


class Mapper():
    def __init__(self, lens = "", clusterer = "DBSCAN", clusterer_params = [], n_rcover = None):
        self.lens = lens
        self.clusterer = clusterer
        self.n_rcover = n_rcover
        self.clusterer_params = clusterer_params

    
    def pullback_cover(self, data):
        N, overlap = self.n_rcover
        frame  = Lens(name = self.lens).fit_project(data)
        Y = frame["projected"].values
        max, min  = np.amax(Y), np.amin(Y)
        epsilon = ((max - min)/N)*overlap
        rcover = [min + (max - min)*i/N for i in range(N)] + [max]
        #print(rcover)
        covering_frames = [None]*N
        for i in range(N):
            temp = frame.loc[frame["projected"] < rcover[i+1] + epsilon]
            covering_frames[i] = temp.loc[frame["projected"] > rcover[i] - epsilon]
        return covering_frames

        
    def cluster(self,data):
        covering = self.pullback_cover(data)
        cluster_frames = [[]]*len(covering)
        index = [[]]*len(covering)
        from sklearn.cluster import DBSCAN
        eps = self.clusterer_params[0]
        min_samples = self.clusterer_params[1]
        for i in range(len(covering)): 
            C = covering[i]["data_points"].values.tolist()

            if C != []:
                dbscan = DBSCAN(eps = eps, min_samples = min_samples).fit(C)
                covering[i]["cluster"] = dbscan.labels_
                cluster_frames[i] = [covering[i][covering[i]["cluster"] == label] for label in set(dbscan.labels_)]
                index[i] = [str(i) + "," + str(j) + "," + str(len(cluster_frames[i][j])) for j in range(len(set(dbscan.labels_)))]
        
        return cluster_frames, index
        
        
    def make_nerve(self,data):

        cluster_frames, index = self.cluster(data)
        
        V = flatten(index)
        
        pairs = [(x,y) for x in V for y in V if V.index(x) < V.index(y)]
        
        E = [(x,y) for (x,y) in pairs if [a for a in cluster_frames[int(x.split(",")[0])][int(x.split(",")[1])]["data_points"].values.tolist() if a in cluster_frames[int(y.split(",")[0])][int(y.split(",")[1])]["data_points"].values.tolist()] != []]
        
        
        return V,E

    
    def write_to_json(self,data):
        V, E = self.make_nerve(data)
        max_weight = max([int(v.split(",")[2]) for v in V])
        nodes = [{"id": v, "group": int(v.split(",")[0]), "weight": int(v.split(",")[2])} for v in V]
        links = [{"source": link[0], "target": link[1], "value": 1} for link in E]


        
        viz = {"rcover": self.n_rcover[0], "max_weight": max_weight, "nodes":nodes, "links": links}

        viz_json = json.dumps(viz)

        file = open("mapperViz.json", 'w')
        file.write(viz_json)
        file.close()

        
    




    
        
