
class ValueTooSmallError(Exception):

    def __init__(self, *args):
        super().__init__(args)


    def __str__(self):

        return f'Valor introducido menor que 10'

n = 0
while n < 10:

    try:
        n = int(input('escrive numero'))
        if n < 10:
            raise ValueTooSmallError

    except ValueTooSmallError as error:
        print(error)






