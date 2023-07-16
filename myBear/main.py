# This is a sample Python script.


# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from Series import Series
from DataFrame import DataFrame


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Création d'une Series
    data = [100, 25, 32, None, 24, 65]
    series = Series(data, "a")

    data2 = [10, 20, 41, 66, 1, 3]
    series2 = Series(data2, "b")

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


    #test1 DataFrame constructeur avec liste de Series
    dataframe = DataFrame([series,series2])
    print(f"test1 : {dataframe.listSeries[0].name}")

    #test2 DataFrame constructeur avec liste colonnes et valeur
    dataframe = DataFrame(["col1", "col2"],[[1,2],[3,4]])
    print(f"test1 : {dataframe.listSeries[0].name}")

    # max dataframe
    print(dataframe.max())

    # min dataframe
    print(dataframe.min())

    #print dataframe
    print(dataframe)
    # test iloc
    dataframe.groupby(
        by=["a", "b"],
        agg={
            "c": min,
            "d": max
        }
    )
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
