import pickle

def load_instance(case, show = False):
    with open("Instancias/Inst_{}-P".format(case), "rb") as fp:
        P = pickle.load(fp)

    with open("Instancias/Inst_{}-C".format(case), "rb") as fp:
        C = pickle.load(fp)
    
    N, T, M = len(P), len(C), max(max(P))

    if show:
        print("N={} \t T={} \t M={}".format(N,T,M))
        print("Matriz de preferencias (P):")
        for i, fila in enumerate(P, start=1):
            print(f"Alumno {i}: {fila}")
        
        print("\nCapacidades de los turnos (C):")
        for i, capacidad in enumerate(C, start=1):
            print(f"Turno {i}: {capacidad}")

    return N, T, M, P, C

def main(case):
    # Pon show=True para ver la instancia concreta
    N, T, M, P, C = load_instance(case, show=True)
    
    # TODO Resuelve el problema utilizando vuelta atrás
    def resolver(N,T,M,P,C):
        mejor={"turnos":None, "total":0}
        def back(N,T,M,P,C,sol,indice):
            con={}
            if len(sol)==N:
                conteo={}
                val=0
                n=0

                for i in sol:
                    val+=P[n][i]
                    n+=1


                for i in sol:
                    if i not in conteo.keys():
                        conteo[i]=1
                    else:
                        conteo[i]+=1



                for i in conteo.keys():
                    if conteo[i]>C[i]:
                        return
                    

                if mejor["turnos"]==None:
                    mejor["turnos"]=sol[:]
                    mejor["total"]=0
                    return

                if val>mejor["total"]:
                    mejor["turnos"]=sol[:]
                    mejor["total"]=val
                    return
                

            if indice>=N:
                return
            
            for i in range(len(sol)-1):
                if P[i][sol[i]]==0:
                    return
                
            for i in sol:
                if i not in con.keys():
                    con[i]=1
                else:
                    con[i]+=1
            for i in con.keys():
                if con[i]>C[i]:
                    return
                
            for j in range(T):
                if C[j]>=1:
                    sol.append(j)
                    back(N,T,M,P,C,sol,indice+1)
                    sol.pop()

        back(N,T,M,P,C,[],0)

        return mejor
    print(resolver(N,T,M,P,C))

    
if __name__ == "__main__":
    #main('0')
    # Descomenta estas lineas para ejecutar las instancias
    #main('1')
    #main('2')
    main('3')
    #main('4')
