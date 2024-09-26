def log(func):
    def wrapper(*args,**kwargs):
        with open('log.txt','a',newline='') as f:
            i=args[0]
            f.write(f'{i}')
            f.close()
        return func(*args,**kwargs)
    return wrapper

@log
def test(cadena):
    return(cadena)

test('prueba1')
test('prueba2')

with open('log.txt') as f:
    print(f.read())



    