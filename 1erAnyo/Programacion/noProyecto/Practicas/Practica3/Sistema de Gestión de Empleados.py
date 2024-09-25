class Empleado: #1
    def __init__(self, salario, bonificacion):
        self.salario = salario
        self.bonificacion = bonificacion

    def __lt__(self, other):
        return self.salario + self.bonificacion < other.salario + other.bonificacion

    def __eq__(self, other):
        return self.salario + self.bonificacion == other.salario + other.bonificacion

    def __add__(self, other):
        return self.bonificacion + other.bonificacion

class EmpleadoRegular(Empleado): #2
    def __init__(self, salario, bonificacion):
        super().__init__(salario, bonificacion)


class Gerente(Empleado): #3
    def __init__(self, salario, bonificacion):
        bonificacion *= salario / 100
        super().__init__(salario, bonificacion)


Empleado1 = Gerente(4000, 20)
Empleado2 = EmpleadoRegular(4000, 800)
Empleado3 = EmpleadoRegular(1500, 200)

print(Empleado3 < Empleado1)
print(Empleado1 == Empleado2)
print(Empleado1 + Empleado3)

