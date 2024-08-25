
mi_archivo = ("mi_archivo.txt")


with open(mi_archivo, "r") as archivo:
    nPalabras = {}
    list = archivo.readlines()
    list2 = []
    for line in list:

        list2.append(line.split(' '))
    for list2 in list:
        for palabra in list2:
            if palabra in nPalabras:
                nPalabras[palabra] += 1
            else:
                nPalabras[palabra] = 1

print(nPalabras)
