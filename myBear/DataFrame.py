from typing import List, Any
from Series import Series

class DataFrame:
    def __init__(self, *args):
        if len(args) == 1:
            self.from_list_series(args[0])
        elif len(args) == 2:
            self.from_lists(args[0], args[1])
        else:
            self.listSeries = []


    def from_list_series(self, listSeries):
        if len(listSeries) > 0:
            size = listSeries[0].size
            if all(series.size == size for series in listSeries):
                self.listSeries = listSeries
                #initialise une dataframe de 0
                self.iloc = [[0] * len(listSeries) for _ in range(size + 1)]
                #ajoute le nom des colonnes
                for i in range(len(listSeries)):
                    self.iloc[0][i] = listSeries[i].name
                #ajoute les valeurs à chaque colonne
                for i in range(1,size):
                    l = []
                    for y in range(len(listSeries)):
                        l.append(listSeries[y].data[i - 1])
                    self.iloc[i] = l
            else:
                print("Les listes ne sont pas de la même taille")
        else:
            self.listSeries = []

    def from_lists(self, listColonnes: List[str], listlistVal: List[List[Any]]):
        if len(listColonnes) == len(listlistVal):
            self.listSeries = []
            for colonne, valeurs in zip(listColonnes, listlistVal):
                series = Series(valeurs, colonne)
                self.listSeries.append(series)
        else:
            print("Les listes ne sont pas de la même taille")

    @property
    def _iloc(self):
        return self.iloc

    def max(self):
        max = self.listSeries[0].max()
        for series in self.listSeries:
            if max <= series.max():
                max = series.max()
        return max

    def min(self):
        min = self.listSeries[0].min()
        for series in self.listSeries:
            if min >= series.min():
                min = series.min()
        return min
