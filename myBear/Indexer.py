class Indexer:
    def __init__(self, parent):
        self.parent = parent

    def __getitem__(self, index):
        row, col = index
        return self.parent.tab[row][col]