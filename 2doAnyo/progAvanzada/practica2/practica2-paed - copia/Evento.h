#ifndef EVENTO_H
#define EVENTO_H

#include "Fecha.h"
#include<string>
#include<vector>
using namespace std;

class Evento{
private:
   Fecha fecha;
   string titulo;
   string descripcion;
   int categoria;

public:
   //Constructor por defecto: fecha 1/1/1900, titulo "sin título", descr vacía, cat -1
   Evento();
   //Constructor sobrecargado
   Evento(const Fecha&, const string&, const string&, int);
   //Constructor de copia
   Evento(const Evento&);
   //Operador de asignación
   Evento& operator=(const Evento &);
   //Destructor: pone la fecha a 1/1/1900, el título a "sin título", descr = "", cat=0
   ~Evento();

   bool operator==(const Evento &) const;
   bool operator!=(const Evento &) const;

   Fecha getFecha() const;
   string getTitulo() const;
   string getDescripcion() const;
   int getCategoria() const;

   void setFecha(const Fecha& );
   void setTitulo(const string &);
   void setDescripcion(const string &);
   void setCategoria(int);

   //Convierte en cadena
   //Formato: "lunes 9 de septiembre de 2024:Título[categoría_en_texto]:Descripción"
   //Si cat=-1, categoría_en_texto=""
   string aCadena(const vector<string>&) const;
};

#endif
