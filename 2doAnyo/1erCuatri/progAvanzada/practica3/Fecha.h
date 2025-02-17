#ifndef FECHA_H
#define FECHA_H

#include <string>
using namespace std;

class Fecha{
   private:
   int dia, mes, anyo;
   bool esFechaCorrecta(int, int, int) const;
   bool esBisiesto(int) const;
   int calculaDiasMes(int, int) const;
   int obtenerDiaSemana() const;
   string nombreMes(int) const;
   string nombreDia(int) const;

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

   bool operator==(const Fecha &) const;
   bool operator!=(const Fecha &) const;
   bool operator<(const Fecha &) const;
   bool operator>(const Fecha &) const;

   int getDia() const;
   int getMes() const;
   int getAnyo() const;

   bool setDia(int);
   bool setMes(int);
   bool setAnyo(int);

   bool incrementaDias(int );
   bool incrementaMeses(int );
   bool incrementaAnyos(int );

   //Devuelve una representación como cadena de la fecha
   // larga = true -> formato largo "lunes 9 de septiembre de 2024"
   // conDia = true -> incluir el nombre del día de la semana
   string aCadena(bool larga, bool conDia) const;
};

#endif
