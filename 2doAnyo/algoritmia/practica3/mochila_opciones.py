import random

class Mochila:
    def __init__(self, v, w, W, N):
        self.v = v
        self.w = w
        self.W = W
        self.N = N   
        self.cota_optimista = 0     
        self.best_valor = -1
        self.best_solucion = None
        self.count = 0

    def optimista(self, x, i, w_acc, v_acc):
        if self.cota_optimista == 1:
            return self.optimista_1(x, i, v_acc)
        elif self.cota_optimista == 2:
            return self.optimista_2(i, w_acc, v_acc)
        else:
            return float('Inf')

    def optimista_1(self, x, i, v_acc):
        while i < self.N:
            v_acc += self.v[i]
            i += 1
        return v_acc

    def optimista_2(self, i, w_acc, v_acc):
        capacidad_restante = self.W - w_acc
        indices = sorted(range(i, len(self.v)), key=lambda j: self.v[j] / self.w[j], reverse=True)
        valor_adicional = 0

        for j in indices:
            if capacidad_restante == 0:
                break
            if self.w[j] <= capacidad_restante:
                capacidad_restante -= self.w[j]
                valor_adicional += self.v[j]
            else:
                valor_adicional += self.v[j] * (capacidad_restante / self.w[j])
                capacidad_restante = 0
        return v_acc + valor_adicional

    def voraz_bueno(self):
        x = [0] * self.N
        v_acc = 0
        w_acc = 0

        indices_ordenados = sorted(range(self.N), key=lambda j: self.v[j] / self.w[j], reverse=True)
        for j in indices_ordenados:
            if w_acc + self.w[j] <= self.W:
                x[j] = 1
                w_acc += self.w[j]
                v_acc += self.v[j]
        return x, v_acc

    def voraz_basico(self):
        x = [0] * self.N
        i = 0
        v_acc = 0
        w_acc = 0
        while i < self.N:
            if w_acc + self.w[i] <= self.W:
                w_acc += self.w[i]
                v_acc += self.v[i]
                x[i] = 1
            else:
                x[i] = 0
            i += 1
        return x, v_acc

    def __resolver_mochila(self, x, i, w_acc, v_acc):
        self.count += 1
        if w_acc <= self.W and self.optimista(x, i, w_acc, v_acc) > self.best_valor:
            if i == self.N:
                if self.best_valor < v_acc:
                    self.best_valor = v_acc
                    self.best_solucion = x.copy()
            else:
                for o in [0, 1]:
                    x[i] = o
                    self.__resolver_mochila(x, i + 1, w_acc + o * self.w[i], v_acc + o * self.v[i])

    def __inicializar(self):
        self.best_valor = -1
        self.best_solucion = None
        self.count = 0
        self.cota_optimista = 0  

    def resolver(self, voraz, optimista):
        self.__inicializar()
        self.cota_optimista = optimista
        x = [-1] * self.N
        if voraz == 1:
            self.best_solucion, self.best_valor = self.voraz_basico()
        elif voraz == 2:
            self.best_solucion, self.best_valor = self.voraz_bueno()

        self.__resolver_mochila(x, 0, 0, 0)

        return self.best_valor, self.best_solucion, self.count

if __name__ == "__main__":
    random.seed(1)
    N = 20
    v = [random.randint(1, 50) for _ in range(N)]
    w = [random.randint(1, 50) for _ in range(N)]
    W = random.randint(N * 1, N * 25)
    mochila = Mochila(v, w, W, N)

    print("Valores (v):", v)
    print("Pesos (w):", w)
    print("Peso máximo (W):", W)
    print()

    for voraz in [0, 1, 2]:
        print()
        for optimista in [0, 1, 2]:
            v, s, c = mochila.resolver(voraz=voraz,optimista=optimista)
            print("Voraz {} - Optimista {}".format(voraz,optimista))
            print("c={} / {}\tv={}\t{}".format(c, 2**(N+1) - 1, v, s))