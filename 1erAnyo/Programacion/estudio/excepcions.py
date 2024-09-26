class ErrrorComun(Exception):
    def __init__(self, mensaje, *args):
        self.mensaje = mensaje
        super().__init__(*args)


    def __str__(self):
        return self.mensaje

