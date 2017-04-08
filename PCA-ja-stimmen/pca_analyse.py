# -*- coding: utf-8 -*-
"""
Created on Sat Apr 08 18:10:05 2017

@author: Thomas
"""
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from numpy import genfromtxt
import numpy as np
from sklearn.decomposition import PCA
import pandas as pd

data = genfromtxt('prozent-ja-stimmen.csv', delimiter=';')
importdata = pd.read_csv('prozent-ja-stimmen.csv', quotechar='"', delimiter=";", encoding="latin-1")
cantons = list(importdata.columns.values)[2:]
data_only = importdata
del data_only['id']
del data_only['Beschreibung']

post_jura_data = data_only.as_matrix()[0:320, ]
pre_jura_data = data_only.as_matrix()[320:, :25]

pca = PCA(n_components=2)
coordinates = pca.fit_transform(post_jura_data.T)

fig, ax = plt.subplots()
index = np.arange(len(cantons))
colors = cm.hsv(np.linspace(0, 1, len(cantons)))
for i, col in zip(index, colors):
    tmp = plt.scatter(coordinates[i, 0], coordinates[i, 1], color=col, label=cantons[i])
#plt.legend()
    plt.text(coordinates[i, 0], coordinates[i, 1], cantons[i])