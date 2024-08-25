

import csv
def csvADict(fichero):

    with open(fichero) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        datalist = []

        for i in reader:


            datalist.append(i)

        dict = {}
        for j in range(len(datalist)):
            if j == 0:
                pass
            else:
                dict[datalist[j][0]] = datalist[j][1:]



        return dict




def dicct(fichero):
    with open(fichero) as textoReader:


        texto = textoReader.read()

        nuevo = texto.split('\n')

        dict = {}
        for palabra in nuevo:
            try:
                dict[palabra] += 1

            except KeyError:
                dict[palabra] = 1


    return dict

def csvcv(dict):
    with open('salida.csv', 'w') as csvFile:

        writer = csv.writer(csvFile, delimiter=',',lineterminator='\n' )

        writer.writerow(['palabra','repeticiones'])
        for i in dict:
            writer.writerow([i,dict[i]])


csvcv(dicct('hola.txt'))

