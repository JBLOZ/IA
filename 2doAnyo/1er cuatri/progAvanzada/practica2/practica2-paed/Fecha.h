#ifndef FECHA_H
#define FECHA_H

#include <string>

using namespace std;

class Fecha{
   private:

   int dia, mes, anyo;
   //Puede ser útil: eliminar si no se han implementado estos métodos auxiliares
   bool esFechaCorrecta(int, int, int) const;
   bool esBisiesto(int) const ;
   int calculaDiasMes(int, int) const;
   int obtenerDiaSemana() const;


   public:
   
   //Constructor por defecto: inicializa la fecha a 1/1/1900
   Fecha();
   
   //Constructor sobrecargado: inicializa la fecha según los parámetros
   Fecha(int dia,int mes,int anyo);
   
   //Constructor de copia
   Fecha(const Fecha &);

   string nombreMes(int m) const;
   string nombreDia(int d) const;
   
   //Destructor: pone la fecha a 1/1/1900
   ~Fecha();

   //Operador de asignación
   Fecha& operator=(const Fecha &);
   
   //Operador de comparación
   bool operator==(const Fecha &) const;
   
   //Operador de comparación
   bool operator!=(const Fecha &) const;
   
   //Operador de comparación
   bool operator<(const Fecha &) const;
   
   //Operador de comparación
   bool operator>(const Fecha &) const;
   
   
   //Devuelve el día
   int getDia() const;
   
   //Devuelve el mes
   int getMes() const;
   
   //Devuelve el año
   int getAnyo() const;
   
   //Modifica el día: devuelve false si la fecha resultante es incorrecta
   bool setDia(int);
   
   //Modifica el mes: devuelve false si la fecha resultante es incorrecta
   bool setMes(int);

  //Modifica el anyo: devuelve false si la fecha resultante es incorrecta
   bool setAnyo(int);

  //Incrementa la fecha en el número de días pasado como parámetro.
  //Si el parámetro es negativo, la decrementa
  bool incrementaDias(int );
  
  //Incrementa la fecha en el número de meses pasado como parámetro.
  //Si el parámetro es negativo, la decrementa
  bool incrementaMeses(int );
 
  //Incrementa la fecha en el número de años pasado como parámetro.
  //Si el parámetro es negativo, la decrementa
  bool incrementaAnyos(int );
  
  //Devuelve una representación como cadena de la fecha
  string aCadena(bool larga, bool conDia) const;
   
};

#endif
