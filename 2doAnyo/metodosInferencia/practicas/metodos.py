import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# probabilidad contagiasre siendo mayor es mayor 
# aleatorizar el numero inicial de contagiados minimo 1

########################################################
#######    Persona
########################################################                
cont_ID=0 #contador de persones i identificador
dist_contagi=0.05
prob_contagi=0.09
temps_contagi=15
class Persona:          

    def __init__(self):
        global cont_ID
        cont_ID +=1
        self.ID=cont_ID
        self.edat=self.edat()
        self.Posx=np.random.rand()
        self.Posy=np.random.rand()
        self.sexe=np.random.choice(['Dona', 'Home'], p=[0.48, 0.52])
        self.estat='sa'                        #sa, infectant, contagiat, mort
        self.Vx=np.random.choice([0.01,-0.01])
        self.Vy=np.random.rand()
        self.col=[1,0,0]  #color
        self.tcont=0     # representa l'instant on s'ha contagiat   
        
    def quies(self):
        print('ID= ',self.ID,' (x,y)= (',self.Posx,',', self.Posy, ')  edat= ',self.edat,' estat= ',self.estat)

    def set_estat(self,estat):
       self.estat=estat
       if estat=='sa':
           self.col=[1,0,0]
       elif estat=='infectat':
           self.col=[0,1,0]
       elif estat=='contagiat':
           self.col=[0,0,1]
       else:
           self.col=[0.9,0.9,0.9]
           
    def move(self):
       self.Posx += self.Vx
       self.Posy += self.Vy       
       if self.Posx <= 0 or self.Posx >= 1:  # Colisión con borde izquierdo o derecho
           self.Vx *=-1
       if self.Posy <= 0 or self.Posy >= 1:  # Colisión con borde izquierdo o derecho
           self.Vy *=-1          
       
    def edat(self):
        e = np.random.normal(40, 10) # distribución normal con media 40 y varianza 10
        if e < 0:
            return 0
        elif e > 104:
            return 104
        else: 
            return e

    def probabilidad_contagio(self):
        prob_base = 0.09

        if self.edat > 40:
            prob_edad = 1 + (self.edat - 40) * 0.01
        else:
            prob_edad = 1 - (40 - self.edat) * 0.005
        
        if self.sexe == 'Dona':
            prob_sexo = prob_base + np.random.uniform(0.05, 0.09)
        else:
            prob_sexo = prob_base - np.random.uniform(0.03, 0.06)

        prob_final = prob_edad * prob_sexo
        return prob_final

########################################################
#######    Agrupacio   Lista de personas con una misma característica. p.e. estar sano
########################################################                
           
class Agrupacio:    
    
    def __init__(self,n,sname):  
        self.caract='sa'  #sa, infectant, contagiat,mort        
        self.Lpers=[]
        for i in range(n):            
            self.Lpers.append(Persona())
        self.name=sname
    def set_estat(self,newstat):
        for pers in self.Lpers:
            pers.set_estat(newstat)
            
    def llista(self):
        for i in range(len(self.Lpers)):
            self.Lpers[i].quies()
        print('La agrupació ',self.name,' té ',len(self.Lpers),' elements')    
    def nindiv(self):
        return len(self.Lpers)        
    
    def persona(self,i):
        return(self.Lpers[i]) 
    
    def move(self):
        for p in self.Lpers:
            p.move()
            
    def set_color(self,scol):
        for p in self.Lpers:
            p.col=scol
    
########################################################
#######    Poblacio
########################################################                
class Poblacio: 
    tt=0    #instant en el que está viviendo. Cada vez que evoluciona, t incrementa
    
    def __init__(self,name,nsanos,ninfectados):    
        self.name=name
        self.AgrupSana=Agrupacio(nsanos,'LSana')
        self.set_agrupinfectada(ninfectados)
        self.AgrupContagiada=Agrupacio(0,'Lcont')
        self.AgrupMorta=Agrupacio(0,'LM')
        self.contactes=0     #Per debug. Conta quantes proximitats s'han produït
        self.AgrupSana.set_color([0,1,0])
        self.AgrupContagiada.set_color([0,0,1])
        self.AgrupInfectada.set_color([1,0,0])
        self.AgrupMorta.set_color([0.9,0.9,0.9])                
        
    def set_agrupsana(self,n):
       self.AgrupSana=Agrupacio(n)
       
    def set_agrupinfectada(self,n):
       self.AgrupInfectada=Agrupacio(n,'LInf')
       self.AgrupInfectada.set_estat('infectada')
       
    def move(self):
        self.AgrupSana.move()
        self.AgrupContagiada.move()
        self.AgrupInfectada.move()
        
    def evoluciona(self):  
        self.tt+=1
        self.move()
        nInf=self.AgrupInfectada.nindiv()
        nSa=self.AgrupSana.nindiv()
        Lcambios=[]
        Laux=[]
       ########################
       #######Sano->Infectado
       ########################
        for p1 in self.AgrupInfectada.Lpers:           
            Laux=[]
            for p2 in self.AgrupSana.Lpers:
                d=dist(p1,p2)
                if (d<dist_contagi) and (np.random.rand()<prob_contagi): #Se produce contacto y contagio
                    Laux.append(p2) 
                    p.set_estat = 'infectat' 
                    p2.col=[1,0,0]                                         
                    p2.tcont=self.tt                                      #Instante que se produce la infección
            self.contactes=len(Laux)                  
            for p in Laux:                                             
                self.AgrupSana.Lpers.remove(p)
                #print('Ix -> ',p.ID)                 
                Lcambios.append(p)
        for p in Lcambios:                                    
            self.AgrupInfectada.Lpers.append(p)        
       ########################
       #######Infect->Contagiat 
       ########################
        Laux=[]
        for p in self.AgrupInfectada.Lpers:
            if self.tt-p.tcont>temps_contagi:
                p.set_estat('contagiat')
                p.col=[0,0,1]
                Laux.append(p)
        for p in Laux:
           self.AgrupContagiada.Lpers.append(p)
           self.AgrupInfectada.Lpers.remove(p)
        ########################
        #######Infectat->Mort 
        ########################
        Laux = []
        for p in self.AgrupInfectada.Lpers:
            # Calcula la probabilidad de muerte dependiendo del tiempo desde la infección
            prob_muerte = self.probabilidad_muerte(p.tcont, self.tt, temps_contagi)
            if np.random.rand() < prob_muerte:  # Decisión de muerte basada en probabilidad dinámica
                p.col = [0.9, 0.9, 0.9]
                p.Vx = 0
                p.Vy = 0
                p.set_estat('mort')
                Laux.append(p)
        
        # Mueve los individuos que han fallecido al grupo de fallecidos
        for p in Laux:
            self.AgrupMorta.Lpers.append(p)
            self.AgrupInfectada.Lpers.remove(p)

    def probabilidad_muerte(self, tt_infeccion, tiempo_actual, temps_contagi):
        """
        Calcula la probabilidad de muerte de una persona en función del tiempo de infección.
        La probabilidad es baja al principio y final, y máxima en la mitad del tiempo de infección.
        """
        t = tiempo_actual - tt_infeccion  # Tiempo desde que la persona fue infectada
        mitad = temps_contagi / 2
        if t >= temps_contagi:
            return 0  # Después de temps_contagi, la probabilidad de muerte es 0
        
        # Parábola que alcanza su máximo en la mitad del tiempo de contagio
        prob_maxima = np.random.rand(0, 1)  # Ajusta la probabilidad máxima a un valor entre 0 y 1
        probabilidad = prob_maxima * (1 - ((t - mitad) / mitad) ** 2) # Probabilidad muerte en función del tiempo
        return max(0, probabilidad)  # Aseguramos que no sea negativa

    

        # Vx y Vy a 0
    def resumen(self):                                                   #Escribe un resumen del estado de la población
       print('Resumen de la población ',self.name)
       print('N pers sanas       = ',self.AgrupSana.caract,self.AgrupSana.nindiv() )
       print('N pers infectadas  = ',self.AgrupInfectada.caract,self.AgrupInfectada.nindiv())
       print('N pers contagiadas = ',self.AgrupContagiada.caract,self.AgrupContagiada.nindiv())
       print('N pers fallecidas  = ',self.AgrupMorta.caract,self.AgrupMorta.nindiv())

    def positions(self)   :
        LP=[]
        cols=[]
        for p in self.AgrupSana.Lpers:
            LP.append([p.Posx,p.Posy])
            cols.append([0,1,0])
        for p in self.AgrupInfectada.Lpers:
            LP.append([p.Posx,p.Posy])
            cols.append([1,0,0])
        for p in self.AgrupContagiada.Lpers:
            LP.append([p.Posx,p.Posy])
            cols.append([0,0,1])
        for p in self.AgrupMorta.Lpers:
            LP.append([p.Posx,p.Posy])
            cols.append([1,1,1])
        return LP,cols
    
    def nPopulation(self):
        return len(self.AgrupContagiada.Lpers)+len(self.AgrupInfectada.Lpers)+len(self.AgrupSana.Lpers)+len(self.AgrupMorta.Lpers)

    def dist_total(self):
        S,Smin,Smax =0,100000000,0        
        for p1 in self.AgrupSana.Lpers:
            for p2 in self.AgrupInfectada.Lpers:
                d=dist(p1, p2)
                S +=d
                if d<Smin: Smin=d
                if d>Smax: Smax=d                    
        return S,Smin,Smax
        
    def foto(self):
        return len(self.AgrupSana.Lpers),len(self.AgrupInfectada.Lpers),len(self.AgrupContagiada.Lpers)
########################################################
#######    FUNCIONES        
########################################################    
def dist(p1,p2):
    return ((p1.Posx-p2.Posx)**2+(p1.Posy-p2.Posy)**2)**(0.5)

       
# Configuración inicial de los puntos: posiciones y velocidades
#np.random.seed(0)  # Para reproducibilidad

########################################################

########################################################
#######    Població
######################################################## 
NN=500           #Nº de individuos en la población
mypoble=Poblacio('Xixona',NN,1)
mypoble.resumen()

########################################################
#######    Draw
########################################################    

N=mypoble.nPopulation()

positions = np.random.rand(N, 2)               # Posiciones iniciales entre [0 y 1]
velocities = ((np.random.rand(N, 2)) * 2-1)/2  # Velocidades aleatorias en el rango [-1, 1]
nn= int(N/2)


Nframes=300     # Nº de pasos a dibujar en un ciclo completo
Nfps=20         # Nº de frames por segundo para visualizar el estado de la población

colors=[]
#for i in range(N) : colors.append([255,0,0])  # Por si quiero poner colores aleatorios en la población

# Configurar la figura y los límites
fig, ax = plt.subplots()
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_title('Pandemy')
ax.color='Red'
scat = ax.scatter(positions[:, 0], positions[:, 1])
i=0    #Nº de frame que estoy actualizando. Inicializado a cero
# Función de actualización para la animación
def update(frame):
    global positions, velocities,i,ax
    # Actualizar posiciones    
    i+=1
    #positions += v
    # Verificar colisiones con los bordes y cambiar dirección
    positions,colors=mypoble.positions()            
    print(i,'---> ',mypoble.foto())    #util para depurar
    scat.set_offsets(positions) 
    scat.set_facecolors(colors)   
    mypoble.evoluciona()  #Mueve las personas y actualiza contagios.

# Crear animación
ani = FuncAnimation(fig, update, frames=Nframes)
ani.save('animation.mp4', writer='ffmpeg', fps=Nfps);


#########################################################
##         Para salvar la animación en formato html
#########################################################
#f=open("provata.html","w")         
#ft=ani.to_jshtml(fps=100,embed_frames=True,default_mode='once')
#f.write(ft)
#f.close()


#########################################################
#   Este código genera un gráfico estático con la evolución de la población. 
#########################################################
mypoble2=Poblacio('Mutxamel',NN,1)
mypoble2.resumen()

positions=[]
colors=[]
for i in range(Nframes): # Mirar si individuos están cerca para ver si hay contagio, si están lejos ni los mires
    san,inf,ctg=mypoble2.foto()
    #print(i,'  -> ',san,inf,ctg)
    mypoble2.evoluciona()
    positions.append([i/Nframes,inf/NN])
    colors.append([1,0,0])
    positions.append([i/Nframes,ctg/NN])
    colors.append([0,0,1])
    positions.append([i/Nframes,san/NN])
    colors.append([0,1,0])
scat.set_offsets(positions)    
scat.set_facecolors(colors) 
plt.show()




print('--------------------------------------')

mypoble.resumen()


print(' Acabat')