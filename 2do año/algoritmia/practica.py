import numpy as np
import matplotlib.pyplot as plt


n = np.linspace(1, 20, 400)


f1 = np.power(n, 1/2)  
f2 = np.power(10, n)   
f3 = np.power(n, 1.5)
f4 = 2 * np.sqrt(np.log2(n))




plt.figure(figsize=(10, 6))


plt.plot(n, f1, label=r'$\sqrt[2]{n}$')
plt.plot(n, f2, label=r'$10^n$')
plt.plot(n, f3, label=r'$n^{1.5}$')
plt.plot(n, f4, label=r'$2\sqrt{\log_2(n)}$')



plt.title('Visualización de Complejidades Teóricas')
plt.xlabel('n')
plt.ylabel('f(n)')


plt.legend()


plt.yscale('log')
plt.savefig('grafica.pdf')
