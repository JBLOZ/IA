#ifndef CALENDARIO_H
#define CALENDARIO_H

#include "Evento.h"
#include "Fecha.h"
#include <string>
#include <vector>
#include <map>
#include <stack>
#include <map>
#include <iostream>
#include <algorithm>
#include <unordered_map>

using namespace std;

class Calendario{
private:
   // Map principal: Fecha->Evento
   map<Fecha,Evento> eventos;
   // Para búsqueda por título: Titulo->(múltiples fechas)
   multimap<string,Fecha> indiceTitulo;

   // Estructuras para deshacer
   // Para deshacer inserciones: almacenamos el evento insertado
   stack<Evento> historialInserciones;
   // Para deshacer borrados: almacenamos el evento borrado
   stack<Evento> historialBorrados;

   // Frecuencias
   // categoría->frecuencia
   map<int,int> freqCat;
   // día->frecuencia
   map<int,int> freqDia;
   // mes->frecuencia
   map<int,int> freqMes;
   // año->frecuencia
   map<int,int> freqAny;

   void incrementarFrecuencias(const Evento &e);
   void decrementarFrecuencias(const Evento &e);
   int masFrecuente(const map<int,int> &m, int vacioValue) const;

public:
   Calendario();
   Calendario(const Calendario&);
   Calendario& operator=(const Calendario &);
   ~Calendario();

   bool insertarEvento(const Evento&);
   bool eliminarEvento(const Fecha&);
   bool comprobarEvento(const Fecha&) const;
   Evento obtenerEvento(const Fecha&) const;
   string aCadena(const vector<string>&) const;

   void deshacerInsercion();
   void deshacerBorrado();

   string aCadenaPorTitulo(const string&, const vector<string>&) const;

   int categoriaMasFrecuente() const;
   int diaMasFrecuente() const;
   int mesMasFrecuente() const;
   int anyoMasFrecuente() const;
};

#endif
