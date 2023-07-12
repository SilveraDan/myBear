from typing import Any


class Series:
    def __init__(self, data, name):
        self.data = data
        self.name = name
        self.size = len(data)
        self.missing_values = self.data.count(None) if None in self.data else 0
    @property
    def iloc(self) -> Any:
        return self.data



    def max(self):
        return max(self.data)

    def min(self):
        return min(self.data)

    def mean(self):
        return sum(self.data) / len(self.data)

    def std(self):
        n = len(self.data)
        if n <= 1:
            return 0

        moyenne = sum(self.data) / n

        somme_carres_ecarts = sum((x - moyenne) ** 2 for x in self.data)

        variance = somme_carres_ecarts / (n - 1)

        ecart_type = variance ** 0.5

        return ecart_type

    def count(self):
        return sum(self.data)