from typing import List, Any
from Series import Series
from Indexer import Indexer



class DataFrame:
    def __init__(self, *args):
        self.iloc = Indexer(self)
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
                self.initTab(size,len(listSeries))
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
                self.initTab(len(valeurs), len(listColonnes))
        else:
            print("Les listes ne sont pas de la même taille")

    def initTab(self,nbrLigne,nbrCol):
        print(nbrLigne)
        print(nbrCol)
        # initialise une dataframe de 0
        self.tab = [[0] * nbrCol for _ in range(nbrLigne)]
        # ajoute le nom des colonnes
        for i in range(nbrCol - 1):
            self.tab[0][i] = self.listSeries[i].name
        # ajoute les valeurs à chaque colonne
        for i in range(1, nbrLigne):
            l = []
            for y in range(nbrCol - 1):
                l.append(self.listSeries[y].data[i - 1])
            if i != nbrLigne:
                self.tab[i] = l
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


    def __str__(self):
        printreturn = ("--- DATAFRAME --- \n")
        for line in self.tab:
            for val in line:
                printreturn+= "    [" + str(val) + " " + str(val) + "] \n"
        printreturn += ("--- FIN DATAFRAME ---")
        return  printreturn

