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
plt.plot(n,f1, label='n^1/2')
plt.plot(n,f2, label='10^n')
plt.plot(n,f3, label='n^1.5')
plt.plot(n,f4, label='2*log2(n)^1/2')
plt.plot(n,f5, label='n^2*log2(n)')
plt.plot(n,f6, label='2^n')
plt.plot(n,f7, label='n^log2(n)')
plt.plot(n,f8, label='n^2')
plt.plot(n,f9, label='2^log2(n)')
plt.plot(n,f10, label='2^2^log2(n)')
plt.plot(n,f11, label='n^5/2')
plt.xlabel('n')
plt.ylabel('Function value')
plt.title('Growth of Different Functions')
plt.grid()


plt.legend()
plt.yscale('log')
plt.show()
