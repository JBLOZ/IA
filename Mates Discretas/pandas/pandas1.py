import pandas as pd


red_social = {
    'userID':   [1, 2, 3, 4],
    'nombre':   ['Juan', 'Ana', 'Luis', 'Pedro'],
    'apellidos':['Perez', 'Gomez', 'Gonzalez', 'Lopez'],
    'edad':     [23, 45, 34, 23],
    'followers':[100, 200, 300, 400],
    'follows':  [50, 100, 150, 200],
    'posts':    [10, 20, 30, 40],
    'likes':   [1000, 2000, 3000, 4000],
    'conexiones':[[2,3],[],[1,3],[1,2]],
}



dataframe = pd.DataFrame(red_social)

print(dataframe[['nombre','apellidos']])


print(dataframe.iloc[0])

for i in range(4):

    print(dataframe.iloc[i])

print(dataframe[['edad']].values.mean())

print
