# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from Series import Series



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Création d'une Series
    data = [100, 25, 32, None, 24, 65]
    series = Series(data, "MySeries")

    #missing values
    print(f"missing values : {series.missing_values}")
    # iloc
    val = series.iloc[2:5]
    print(f"Valeur à l'index 2 : {val}")

    # max
    print(f"max : {series.max()}")

    # min
    print(f"in : {series.min()}")

    # mean
    print(f"mean : {series.mean()}")

    # ecart type
    print(f"ecart type : {series.std()}")

    # count
    print(f"count : {series.count()}")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
