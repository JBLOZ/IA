import random

class Mochila:
    def __init__(self, v, w, W, N):
        self.v = v
        self.w = w
        self.W = W
        self.N = N
        self.count = 0
        self.cogidos = [-1] * N  # Usado en backtracking
        self.valor_total = 0  # Valor total actual
        self.mejor_valor = 0  # Mejor valor total encontrado
        self.mejor_cogidos = [-1] * N  # Mejores fracciones de los ítems
        self.orden = []  # Orden después de ordenar por valor/peso
        self.solucion = []  # Solución final en orden original

    def __inicializar(self):
        self.count = 0

    def ordenar(self):
        orden = sorted(range(self.N), key=lambda x: self.v[x]/self.w[x], reverse=True)
        nueva_v = [self.v[i] for i in orden]
        nueva_w = [self.w[i] for i in orden]
        self.orden = orden
        return nueva_v, nueva_w

    def backTrakingBackPack(self, v, w, W, i):
        self.count += 1

        if W == 0 or i >= self.N:
            if self.valor_total > self.mejor_valor:
                self.mejor_valor = self.valor_total
                self.mejor_cogidos = self.cogidos
            return

        if w[i] <= W:
            self.cogidos[i] = 1.0
            self.valor_total += v[i]
            self.backTrakingBackPack(v, w, W - w[i], i + 1)

        else:
            # Tomar una fracción del ítem
            fraccion = W / w[i]
            self.cogidos[i] = fraccion
            self.valor_total += v[i] * fraccion
            if self.valor_total > self.mejor_valor:
                self.mejor_valor = self.valor_total
                self.mejor_cogidos = self.cogidos


    def resolver(self):
        self.__inicializar()
        nueva_v, nueva_w = self.ordenar()
        self.backTrakingBackPack(nueva_v, nueva_w, self.W, 0)

        solucion = [0] * self.N
        for idx in range(len(self.orden)):
            original_idx = self.orden[idx]
            frac = self.mejor_cogidos[idx]
            solucion[original_idx] = frac if frac != -1 else 0
        self.solucion = solucion

if __name__ == "__main__":
    random.seed(2)
    N = 50
    v = [random.randint(1,50) for _ in range(N)]
    w = [random.randint(1,50) for _ in range(N)]
    W = random.randint(N*1, N*10)

    mochila = Mochila(v,w,W,N)
    mochila.resolver()
    print("v={}".format(v))
    print("w={}".format(w))
    print("W={}".format(W))
    print("Solucion: {}".format(mochila.solucion))
    print("Valor: {}".format(mochila.mejor_valor))
    print("Llamadas: {}".format(mochila.count))
