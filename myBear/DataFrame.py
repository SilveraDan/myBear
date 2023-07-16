import csv
from typing import List, Any
from Series import Series
from Indexer import Indexer
import json

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
                self.initTab(size, len(listSeries))
            else:
                print("Les listes ne sont pas de la même taille")
        else:
            self.listSeries = []

    def from_lists(self, listColonnes: List[str], listlistVal: List[List[Any]]):
        if len(listColonnes) == len(listlistVal):
            self.listSeries = []
            for colonne, valeurs in zip(listColonnes, listlistVal):
                series = Series(valeurs, colonne)
                print(series.data)
                self.listSeries.append(series)
            self.initTab(len(valeurs) + 1, len(listColonnes))
        else:
            print("Les listes ne sont pas de la même taille")

    def initTab(self, nbrLigne, nbrCol):
        # initialise une dataframe de 0
        self.tab = [[0] * nbrCol for _ in range(nbrLigne)]
        # ajoute le nom des colonnes
        for i in range(nbrCol):
            self.tab[0][i] = self.listSeries[i].name
        # ajoute les valeurs à chaque colonne
        for i in range(1, nbrLigne):
            l = []
            for y in range(nbrCol):
                l.append(self.listSeries[y].data[i - 1])
            if i != nbrLigne:
                self.tab[i] = l
    @property
    def _iloc(self):
        return self.iloc

    def max(self):
        max_list = []
        for series in self.listSeries:
            max_list.append(series.max())
        max_series = Series(max_list, "Max")
        return max_series

    def min(self):
        min_list = []
        for series in self.listSeries:
            min_list.append(series.min())
        min_series = Series(min_list, "Min")
        return min_series

    def mean(self):
        mean_list = []
        for series in self.listSeries:
            mean_list.append(series.mean())
        mean_series = Series(mean_list, "Mean")
        return mean_series

    def count(self):
        count_list = []
        for series in self.listSeries:
            count_list.append(series.count())
        count_series = Series(count_list, "Count")
        return count_series

    def std(self):
        std_list = []
        for series in self.listSeries:
            std_list.append(series.std())
        std_series = Series(std_list, "Count")
        return std_series

    def read_csv(path: str,delimiter: str = ","):
        with open(path, 'r') as fichier:
            lecteur = csv.reader(fichier)
            colonnes = next(lecteur)
            valeurs = [[] for _ in colonnes]

            for ligne in lecteur:
                for i, valeur in enumerate(ligne):
                    valeurs[i].append(valeur)

        return DataFrame(colonnes, valeurs)

    def read_json(path: str, orient: str = "records"):
        with open(path, 'r') as fichier:
            data = json.load(fichier)

            colonnes = list(data.keys())
            valeurs = [[] for _ in colonnes]

            for colonne, valeurs_dict in data.items():
                for valeur in valeurs_dict.values():
                    valeurs[colonnes.index(colonne)].append(valeur)

        return DataFrame(colonnes, valeurs)

    def __str__(self):
        printreturn = ("--- DATAFRAME --- \n")
        for line in self.tab:
            printreturn += "   ["
            for val in line:
                printreturn += str(val) + " "
            printreturn += "] \n"
        printreturn += ("--- FIN DATAFRAME ---")
        return printreturn
