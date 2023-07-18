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
        return max(self.filtered_data())

    def min(self):
        return min(self.filtered_data())

    def mean(self):
        data = self.filtered_data()
        return sum(data) / len(data)

    def std(self):
        data = self.filtered_data()
        n = len(data)
        if n <= 1:
            return 0

        moyenne = sum(data) / n

        somme_carres_ecarts = sum((x - moyenne) ** 2 for x in data)

        variance = somme_carres_ecarts / (n - 1)

        ecart_type = variance ** 0.5

        return ecart_type

    def count(self):
        return sum(self.filtered_data())

    def filtered_data(self):
        return [x for x in self.data if x is not None]

    def __str__(self):
        return f"col : {self.name} , vals : {self.data}"
