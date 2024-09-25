import numpy as np
import matplotlib.pyplot as plt


n = np.linspace(1, 20, 400)


f1 = np.power(n, 1/2)
f2 = np.power(10, n)
f3 = np.power(n, 1.5)
f4 = 2 * np.sqrt(np.log2(n))
f5 = np.power(n,2)*np.log2(n)*n
f6 = np.power(2,n)
f7 = np.power(n,np.log2(n))
f8 = np.power(n,2)
f9 = np.power(2,np.log2(n))
f10 = np.power(2,np.power(2,np.log2(n)))
f11 = np.power(n,5/2)
f12 = np.power(n,2) *np.log2(n)


plt.figure(figsize=(10, 6))


plt.plot(n, f1, label=r'$\sqrt[2]{n}$')
plt.plot(n, f2, label=r'$10^n$')
plt.plot(n, f3, label=r'$n^{1.5}$')
plt.plot(n, f4, label=r'$2\sqrt{\log_2(n)}$')
plt.plot(n, f5, label=r'$n^2 \log_2(n) n$')
plt.plot(n, f6, label=r'$2^n$')
plt.plot(n, f7, label=r'$n^{\log_2(n)}$')
plt.plot(n, f8, label=r'$n^2$')
plt.plot(n, f9, label=r'$2^{\log_2(n)}$')
plt.plot(n, f10, label=r'$2^{2^{\log_2(n)}}$')
plt.plot(n, f11, label=r'$n^{5/2}$')
plt.plot(n, f12, label=r'$n^2 \log_2(n)$')



plt.title('Visualización de Complejidades Teóricas')
plt.xlabel('n')
plt.ylabel('f(n)')


plt.legend()


plt.yscale('log')
plt.savefig('grafica.pdf')
