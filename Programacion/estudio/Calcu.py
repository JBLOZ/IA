
import json
import csv

class Calculadora:

    @staticmethod
    def solicitar(func):
        def interna(*args, **kwargs):
            if len(args) == 0:
                num1, num2 = (float(input('num1: ')), float(input('num2: ')))
                return func(num1, num2)
            else:
                return func(*args)
        return interna

    class guardar_en:
        archivo = 'resultados.txt'

        @classmethod
        def principal(cls,func,tipo):
            cls.tipo = tipo
            def interna(*args, **kwargs):
                resultado = func(*args)
                with open(cls.archivo, 'a') as rstw:
                    if [cls.tipo == 1]:
                        rstw.write(f'{resultado[0]}: {resultado[1]}\n')
                    elif cls.tipo == 2:
                        rstw.write(f'{resultado[0]},{resultado[1]}\n')
                    elif cls.tipo == 3:
                        json.dump({resultado[0]:resultado[1]},rstw)
            return interna


        @classmethod
        def txt(cls,func):
            cls.archivo = 'resultados.txt'
            return cls.principal(func,1)

        @classmethod
        def csv(cls,func):
            cls.archivo = 'resultados.csv'
            return cls.principal(func,2)

        @classmethod
        def json(cls,func):
            cls.archivo = 'resultados.json'
            return cls.principal(func,3)



    @staticmethod
    def quitar_listas(func):
        def interna(*args, **kwargs):
            if len(args) == 1 and type(args[0]) == list:
                return func(*args[0])
            else:
                return func(*args)
        return interna

    @solicitar
    @quitar_listas
    @guardar_en.txt
    @staticmethod
    def suma(*args):
        suma = 0
        for i in args:
            suma += i
        return ('suma', suma)

    @solicitar
    @quitar_listas
    @guardar_en.txt
    @staticmethod
    def resta(*args):
        if len(args) == 0:
            return ('resta', 0)
        resta = args[0]
        for i in args[1:]:
            resta -= i
        return ('resta', resta)

    @solicitar
    @quitar_listas
    @guardar_en.txt
    @staticmethod
    def multiplicar(*args):
        multi = 1
        for i in args:
            multi *= i
        return ('multiplicacion', multi)

    @solicitar
    @quitar_listas
    @guardar_en.txt
    @staticmethod
    def promedio(*args):
        suma = sum(args)
        promedio = suma / len(args)
        return ('promedio', promedio)

    @solicitar
    @quitar_listas
    @guardar_en.txt
    @staticmethod
    def maximo(*args):
        return ('maximo', max(args))

    @solicitar
    @quitar_listas
    @guardar_en.txt
    @staticmethod
    def minimo(*args):
        return ('minimo', min(args))



print(Calculadora.promedio([1,1,3,4,3,4,5]))
