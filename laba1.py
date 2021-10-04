import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import scipy.spatial
import math


def manhattan(a, b):
    distance = 0
    for i in range(len(a)):
        distance += abs(a[i] - b[i])
    return distance


def euclidean(a, b):
    distance = 0
    for i in range(len(a)):
        distance += pow(a[i] - b[i], 2)
    return math.sqrt(distance)


def cosine(a, b):
    distance = scipy.spatial.distance.cosine(a, b)
    return distance


laptopTree = [["Встроенная", "Дискретная"],
              ["Высокая", "Низкая"],
              ["Ноутбуки", "Ультрабуки", "Геймерские"],
              [4, 8, 16, 32],
              ["AMD", "Intel"]]

weights = [0.4, 0.3, 0.3, 0.3, 0.1]


def diff_tree(t1, t2):
    difftree = []
    for i in range(0, 5):
        difftree.append(abs(laptopTree[i].index(t1[i]) - laptopTree[i].index(t2[i])))
    similarity = 0
    for i in range(len(difftree)):
        similarity += difftree[i] * weights[i]
    return similarity


def printCorrelationMatrix(ds, metric):
    matr = []
    for i in range(len(ds.values.tolist())):
        r = []
        for k in range(len(ds.values.tolist())):
            r.append(metric(ds.values.tolist()[i], ds.values.tolist()[k]))
        matr.append(np.array(r))
    matr = np.array(matr)

    plt.imshow(matr)
    plt.title(metric)
    plt.xticks(np.arange(0, len(ds.values.tolist())), rotation=-45)
    plt.yticks(np.arange(0, len(ds.values.tolist())))
    figure(figsize=(10, 10), dpi=160)
    plt.show()


dataSetFromTxt = pd.read_csv('laptops.txt', delimiter='\t', encoding="utf-16-le")
ds = dataSetFromTxt.copy(deep=True)
del ds["Ноутбук"]
del ds["Теги"]

ds["Тип видеокарты"], _ = pd.factorize(ds["Тип видеокарты"])
ds["Цена"], _ = pd.factorize(ds["Цена"])
ds["Категория"], _ = pd.factorize(ds["Категория"])
ds["DDR4"], _ = pd.factorize(ds["DDR4"])
ds["ЗУ"], _ = pd.factorize(ds["ЗУ"])
ds["Количество ОЗУ"] = ds["Количество ОЗУ"].values / max(ds["Количество ОЗУ"].values)
ds["Диагональ больше 14?"], _ = pd.factorize(ds["Диагональ больше 14?"])
ds["Количество на складе"] = ds["Количество на складе"].values / max(ds["Количество на складе"].values)
ds["Есть подсветка клавиатуры"], _ = pd.factorize(ds["Есть подсветка клавиатуры"])
ds["Есть отпечаток пальца"], _ = pd.factorize(ds["Есть отпечаток пальца"])
ds["Процессор"], _ = pd.factorize(ds["Процессор"])
ds["Есть Ethernet"], _ = pd.factorize(ds["Есть Ethernet"])
ds["Объем ЗУ"] = ds["Объем ЗУ"].values / max(ds["Объем ЗУ"].values)
ds["Цвет"], _ = pd.factorize(ds["Цвет"])
print(ds)

printCorrelationMatrix(ds, manhattan)

printCorrelationMatrix(ds, euclidean)

printCorrelationMatrix(ds, cosine)

printCorrelationMatrix(dataSetFromTxt, diff_tree)
