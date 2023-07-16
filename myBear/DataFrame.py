from typing import List, Any
from Series import Series
from Indexer import Indexer
from collections import defaultdict
from typing import Callable, Dict, Any, List
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
                self.listSeries.append(series)
            self.initTab(len(valeurs), len(listColonnes))
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
            printreturn += "   ["
            for val in line:
                printreturn += str(val) + " "
            printreturn += "] \n"
        printreturn += ("--- FIN DATAFRAME ---")
        return printreturn

    def groupby(self, by: List[str] | str, agg: Dict[str, Callable[[List[Any]], Any]]) -> 'DataFrame':
        """
        Regrouper les données en fonction des colonnes spécifiées et appliquer les fonctions d'agrégation aux colonnes spécifiées.

        Args:
            by (List[str] | str): Les colonnes à utiliser pour le regroupement.
            agg (Dict[str, Callable[[List[Any]], Any]]): Les fonctions d'agrégation à appliquer aux colonnes spécifiées.

        Returns:
            DataFrame: Un DataFrame contenant les données regroupées et agrégées.
        """
        if isinstance(by, str):
            by = [by]

        # Récupérer les colonnes utilisées pour le regroupement
        list_columns_to_group = [series for series in self.data if series.name in by]
        # Récupérer les colonnes utilisées pour l'agrégation
        columns_to_aggregate = [series for series in self.data if series.name not in by]

        list_columns_data = []
        # Récupérer les indices de groupe pour chaque combinaison de valeurs de colonnes de regroupement
        group_indices = self.get_group_indices(list_columns_to_group)

        for group_values, indices in group_indices:
            aggregated_values = []
            for column in columns_to_aggregate:
                # Récupérer les valeurs de colonne correspondant aux indices de groupe
                column_values = [int(column.data[i]) for i in indices]
                # Appliquer la fonction d'agrégation à ces valeurs
                agg_func = agg[column.name]
                aggregated_values.append(agg_func(column_values))

            # Combiner les valeurs de groupe et les valeurs agrégées dans un tuple
            group_data = tuple(group_values) + tuple(aggregated_values)

            list_columns_data.append(group_data)

        # Transposer les données regroupées pour obtenir une liste de colonnes
        transposed_grouped_data = list(zip(*list_columns_data))

        # Créer les noms de colonnes pour le DataFrame regroupé
        group_names = by + list(agg.keys())

        # Créer un DataFrame à partir des données regroupées
        return DataFrame(
            [Series(list(serie_data), name=serie_name) for serie_data, serie_name in
             zip(transposed_grouped_data, group_names)], "DataFrame_grouped_by"
        )

    @staticmethod
    def get_group_indices(group_columns: List[Series]) -> List[tuple]:
        """
        Récupérer les indices de groupe pour chaque combinaison de valeurs de colonnes de regroupement.

        Args:
            group_columns (List[Series]): Les colonnes de regroupement.

        Returns:
            List[tuple]: Une liste de tuples contenant les valeurs de groupe et les indices correspondants.
        """
        unique_groups = []
        group_indices = []
        for i, row in enumerate(zip(*[column.data for column in group_columns])):
            if row not in unique_groups:
                unique_groups.append(row)
                group_indices.append([i])
            else:
                group_index = unique_groups.index(row)
                group_indices[group_index].append(i)

        return zip(unique_groups, group_indices)

    def join(self, other: 'DataFrame', left_on: List[str] | str, right_on: List[str] | str,
             how: str = 'left') -> 'DataFrame':
        """
            Joindre les données avec un autre DataFrame en utilisant les colonnes spécifiées.

            Args:
                other (DataFrame): DataFrame à joindre.
                left_on (List[str] | str): Les colonnes à utiliser dans le DataFrame de gauche pour la jointure.
                right_on (List[str] | str): Les colonnes à utiliser dans le DataFrame de droite pour la jointure.
                how (str): Le type de jointure à effectuer. inner, left, right, outer (par défault left)

            Returns:
                DataFrame: Un DataFrame contenant les données de jointure.

            Raises:
                ValueError: Si une colonne spécifiée dans le DataFrame de gauche n'est pas trouvée dans le DataFrame de droite.
                ValueError: Si une colonne spécifiée dans le DataFrame de droite n'est pas trouvée dans le DataFrame de droite.
                ValueError: Si le type de jointure spécifié est invalide is not in (inner, left, right, outer).
        """

        left_columns_indices = []
        right_columns_indices = []

        if isinstance(left_on, str):
            left_on = [left_on]

        if isinstance(right_on, str):
            right_on = [right_on]

        # Récupérer les indices des colones de jointure de la table gauche
        for column in left_on:
            # si le nom de la colone n'est pas dans les colonne du DataFrame gauche on retourne une erreur
            if column not in self.columns.split():
                raise ValueError(f"Column '{column}' not found in the left DataFrame")
            left_columns_indices.append(self.columns.split().index(column))

        # Récupérer les indices des colones de jointure de la table droite
        for column in right_on:
            # si le nom de la colone n'est pas dans les colonne du DataFrame de droite on retourne une erreur
            if column not in other.columns.split():
                raise ValueError(f"Column '{column}' not found in the right DataFrame")
            right_columns_indices.append(other.columns.split().index(column))

        # liste pour collecter les données de jointure
        joined_data = []

        # Récupérer les données de la table gauche (liste de valeur de chaque Serie)
        left_data = list(zip(*[series.data for series in self.data]))

        # Récupérer les données de la table droite //
        right_data = list(zip(*[series.data for series in other.data]))

        # Selon chaque type de jointure

        # Jointure interne : garder uniquement les lignes avec les valeurs correspondantes dans les colonnes de jointure

        if how == 'inner':
            for left_row in left_data:
                for right_row in right_data:
                    matching = True
                    for left_index, right_index in zip(left_columns_indices, right_columns_indices):
                        if left_row[left_index] != right_row[right_index]:
                            matching = False
                            break
                    if matching:
                        joined_data.append(left_row + right_row)

        # Jointure gauche : garder toutes les lignes du DataFrame gauche et les lignes correspondantes dans le DataFrame de droite

        elif how == 'left':
            for left_row in left_data:
                matching_rows = []
                for right_row in right_data:
                    matching = True
                    for left_index, right_index in zip(left_columns_indices, right_columns_indices):
                        if left_row[left_index] != right_row[right_index]:
                            matching = False
                            break
                    if matching:
                        matching_rows.append(left_row + right_row)

                if matching_rows:
                    joined_data.extend(matching_rows)
                else:
                    joined_data.append(list(left_row) + ([None] * len(right_data[0])))

        # Jointure droite : garder toutes les lignes du DataFrame droite et les lignes correspondantes dans le DataFrame de gauche

        elif how == 'right':
            for right_row in right_data:
                matching_rows = []
                for left_row in left_data:
                    matching = True
                    for left_index, right_index in zip(left_columns_indices, right_columns_indices):
                        if left_row[left_index] != right_row[right_index]:
                            matching = False
                            break
                    if matching:
                        matching_rows.append(left_row + right_row)

                if matching_rows:
                    joined_data.extend(matching_rows)
                else:
                    joined_data.append(([None] * len(left_data[0])) + list(right_row))

        #
        elif how == 'outer':
            for left_row in left_data:
                matching_rows = []
                for right_row in right_data:
                    matching = True
                    for left_index, right_index in zip(left_columns_indices, right_columns_indices):
                        if left_row[left_index] != right_row[right_index]:
                            matching = False
                            break
                    if matching:
                        matching_rows.append(left_row + right_row)

                if matching_rows:
                    joined_data.extend(matching_rows)
                else:
                    joined_data.append(list(left_row) + ([None] * len(right_data[0])))

            for right_row in right_data:
                matching_rows = []
                for left_row in left_data:
                    matching = True
                    for left_index, right_index in zip(left_columns_indices, right_columns_indices):
                        if left_row[left_index] != right_row[right_index]:
                            matching = False
                            break
                    if matching:
                        matching_rows.append(left_row + right_row)

                if not any(matching_row == joined_row for joined_row in joined_data for matching_row in matching_rows):
                    joined_data.append(([None] * len(left_data[0])) + list(right_row))

        else:
            raise ValueError(f"Invalid join type '{how}'")

        joined_columns = self.columns + '\t' + other.columns
        joined_columns = list(c for c in joined_columns if c != '\t')

        joined_series = []
        for indice_column_name, column_data in enumerate(zip(*joined_data)):
            joined_series.append(Series(list(column_data), joined_columns[indice_column_name]))

        return DataFrame(joined_series, 'Joined DataFrame: ')