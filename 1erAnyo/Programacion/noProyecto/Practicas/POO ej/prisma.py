class Circulo:
    def __init__(self, radio):
        self.radio = radio

    def calcula_area(self):
        area = 3.14 * (self.radio ** 2)
        return area

    def calcula_perimetro(self):
        perimetro = 2 * 3.14 * self.radio
        return perimetro

class Poliedro:
    def __init__(self, altura, anchura, profundidad):
        self.altura = altura
        self.anchura = anchura
        self.profundidad = profundidad

    def calcula_volumen(self):
        volumen = self.profundidad * self.anchura * self.altura

        return volumen

    def calcula_proporciones(self,escala):
        self.altura *= escala
        self.anchura *= escala
        self.profundidad *= escala

        proporciones = (self.altura, self.anchura, self.profundidad)
        return proporciones


class PrismaRectangular(Poliedro):
    def __init__(self, altura, anchura, profundidad):
        super().__init__(altura, anchura, profundidad)

class Cubo(Poliedro):
    def __init__(self, lado):
        super().__init__(lado, lado, lado)

class Cono(Circulo, Poliedro):
    def __init__(self, radio, altura):
        Circulo.__init__(self, radio)
        Poliedro.__init__(self, altura, 0, 0)

    def calcula_volumen(self):
        volumen = (1/3) * (3.14 * (self.radio ** 2)) * self.altura
        return volumen
    def calcula_proporciones(self, escala):
        self.radio *= escala
        self.altura *= escala
        proporciones = (self.radio, self.altura)
        return proporciones

    def __add__(self, other):
        return self.append(other)







circulo = Circulo(5)
poliedro = Poliedro(5, 5, 5)
cono = Cono(circulo.radio, poliedro.altura)


print(cono + circulo)
print(cono.calcula_proporciones(2))




