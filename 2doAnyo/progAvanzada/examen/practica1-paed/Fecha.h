#ifndef FECHA_H
#define FECHA_H

#include <string>

using namespace std;

class Fecha{
   private:


   /*
   Se pueden emplear otras representaciones, pero tres atributos separados
   para día, mes y año es la representación más adecuada.
   Elimina el comentario del principio de la línea siguiente para definir estos tres atributos:  */
   int dia, mes, anyo;


   /* Funciones auxiliares.
   No es obligatorio emplearlas, pero pueden facilitar mucho la implementación de los métodos públicos.
   Elimina el comentario del principio de cada una si deseas emplearla.*/

   /* Comprueba si el día, mes y año pasados como parámetros representan una fecha váida */
   bool esFechaCorrecta(int, int, int) const;

   /* Determina si el año pasado como parámetro es bisiesto */
   bool esBisiesto(int) const ;

   /* Calcula cuántos días tiene el mes del año pasados como parámetro
   (el año se necesita porque el número de días de febrero depende de si el año es bisiesto) */
   int calculaDiasMes(int, int) const;

   string nombreMes(int) const;

   /* Calcula el día de la semana que corresponde a la fecha actual (0=lunes, 6=domingo) */
   int obtenerDiaSemana() const;


   public:

   //Constructor por defecto: inicializa la fecha a 1/1/1900
   Fecha();

   //Constructor sobrecargado: inicializa la fecha según los parámetros
   Fecha(int dia,int mes,int anyo);

   //Constructor de copia
   Fecha(const Fecha &);

   //Destructor: pone la fecha a 1/1/1900
   ~Fecha();

   //Operador de asignación
   Fecha& operator=(const Fecha &);

   //Operador de comparación
   bool operator==(const Fecha &) const;

   //Operador de comparación
   bool operator!=(const Fecha &) const;

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
