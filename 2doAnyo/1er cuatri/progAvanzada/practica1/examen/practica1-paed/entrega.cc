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
   
   string nombreDia(int d) const;

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
#include<iostream>
using namespace std;

int main(){
   int d,m,a, inc;
   
   cin >> d;
   cin >> m;
   cin >>a;
   cin >> inc;
   
   Fecha f(d,m,a);
   f.incrementaDias(inc);
   cout << f.aCadena(false,false) << endl;
   
   return 0;
}
#include<string>
#include <iostream>
using namespace std;


/*
Métodos privados
Si decides implementar los métodos privados que se proponen en el fichero Fecha.h,
puedes hacerlo aquí.

Asegúrate de añadir el código correspondiente en el interior de cada método
*/


bool Fecha::esFechaCorrecta(int dia,int mes,int anyo) const
{
    if (anyo>=1900 && mes>=1 && mes<=12 && dia>=1)
    {
        if (dia <= Fecha::calculaDiasMes(mes, anyo))
        {   
            
            return true;
        }
    }
    return false;
}



bool Fecha::esBisiesto(int a) const
{
    return (a%4==0 && (a%100 !=0 || a%400== 0));
}



int Fecha::calculaDiasMes(int m, int a) const{
    switch (m)
    {
        case 1:
        case 3:
        case 5:
        case 7:
        case 8:
        case 10:
        case 12:
        return 31;
        case 2:
        if (Fecha::esBisiesto(a)) {return 29;}
        else {return 28;}
        case 4:
        case 6:
        case 9:
        case 11:
        return 30;
        default:
        return -1;
    }
}


string Fecha::nombreMes(int m) const
{
    switch (m)
    {
    case 1:
    return "enero";
    case 2:
    return "febrero";
    case 3:
    return "marzo";
    case 4:
    return "abril";
    case 5:
    return "mayo";
    case 6:
    return "junio";
    case 7:
    return "julio";
    case 8:
    return "agosto";
    case 9:
    return "septiembre";
    case 10:
    return "octubre";
    case 11:
    return "noviembre";
    case 12:
    return "diciembre";
    default:
    return "mes incorrecto";
        
    }
}
string Fecha::nombreDia(int d) const
{
    switch (d)
    {
        case 0:
        return "lunes ";
        break;
        case 1:
        return "martes ";
        break;
        case 2:
        return "miércoles ";
        break;
        case 3:
        return "jueves ";
        break;
        case 4:
        return "viernes ";
        break;
        case 5:
        return "sabado ";
        break;
        case 6: 
        return "domingo ";
        break;
        default:
        return "dia incorrecto";
    }
}


int Fecha::obtenerDiaSemana() const 
{
    int d = dia;
    int m = mes;
    int y = anyo;
    int f;

    if (m < 3) 
    {
        m += 12;
        y -= 1;
    }

    int K = y % 100;
    int J = y / 100;


    f = d + (13 * (m + 1) / 5) + K + (K / 4) + (J / 4) - 2 * J;
    f = (f + 5) % 7;

    return f;
}

/*
Métodos públicos
*/
Fecha::Fecha(){
    dia = 1;
    mes = 1;
    anyo = 1900;
}

Fecha::Fecha(int d,int m,int a){
    if (Fecha::esFechaCorrecta(d,m,a))
    {
        dia = d;
        mes = m;
        anyo = a;
    }
    else
    {
        dia = 1;
        mes = 1;
        anyo = 1900;
    }
}

Fecha::Fecha(const Fecha &f){
    if (Fecha::esFechaCorrecta(f.dia,f.mes,f.anyo))
    {
        dia = f.dia;
        mes = f.mes;
        anyo = f.anyo;
    }
    else
    {
        dia = 1;
        mes = 1;
        anyo = 1900;
    }
}


Fecha::~Fecha(){
    dia = 1;
    mes = 1;
    anyo = 1900;
}

Fecha& Fecha::operator=(const Fecha &f){
    if (Fecha::esFechaCorrecta(f.dia,f.mes,f.anyo))
    {
        this->dia = f.dia;
        this->mes = f.mes;
        this->anyo = f.anyo;
    }
    return *this;
}

int Fecha::getDia() const
{
    return dia;
}

int Fecha::getMes() const
{
    return mes;
}

int Fecha::getAnyo() const
{
    return anyo;
}


bool Fecha::setDia(int d)
{
    if (Fecha::esFechaCorrecta(d,mes,anyo))
    {
        dia = d;
        return true;
    }
    return false;
}

bool Fecha::setMes(int m){

    if (Fecha::esFechaCorrecta(dia,m,anyo))
    {
        mes = m;
        return true;
    }
    return false;
}

bool Fecha::setAnyo(int a){
   if (Fecha::esFechaCorrecta(dia,mes,a))
   {
        anyo = a;
        return true;
   }
    return false;
}


bool Fecha::operator==(const Fecha &f) const
{
    if (f.dia == this->dia && f.mes == this->mes && f.anyo == this->anyo)
    {
        return true;
    }
    else 
    {
        return false;
    }

}

bool Fecha::operator!=(const Fecha &f) const
{
    if (f.dia != this->dia || f.mes != this->mes || f.anyo != this->anyo)
    {
        return true;
    }
    else
    {
        return false;
    }
}


bool Fecha::incrementaDias(int inc)
{
    int dias_incremento, copia_dia, copia_mes, copia_anyo;
    copia_dia = dia;
    copia_mes = mes;
    copia_anyo = anyo;
    dias_incremento = dia + inc;
    if (inc > 0)
    {
        
        while (dias_incremento > Fecha::calculaDiasMes(mes,anyo))
        {
            dias_incremento -= Fecha::calculaDiasMes(mes,anyo);
            if (mes == 12)
            {
                mes = 1;
                anyo += 1;
            }
            else
            {
                mes += 1;
            }
        }
        
    }
    else if (inc<0)
    {
        while (dias_incremento <= 0)
        {
            if (mes == 1)
            {
                mes = 12;
                anyo -=1;
            }
            else
            {
                mes -= 1;
            }
            dias_incremento += Fecha::calculaDiasMes(mes,anyo);
        }
        
    }
    dia = dias_incremento;
    if (Fecha::esFechaCorrecta(dia,mes,anyo))
    {
        return true;
    }
    else
    {
        dia = copia_dia;
        mes = copia_mes;
        anyo = copia_anyo;
        return false;


    }

}


bool Fecha::incrementaMeses(int inc)
{
    if (Fecha::esFechaCorrecta(dia,mes+inc,anyo))
    {
        mes += inc;
        return true;
    }

    return false;
}

bool Fecha::incrementaAnyos(int inc)
{
    if (Fecha::esFechaCorrecta(dia,mes,anyo+inc))
    {
        anyo += inc;
        return true;
    }

    return false;
}


string Fecha::aCadena(bool larga, bool conDia) const
{

   string cadena, dia_semanal;
   int entero;
   entero = Fecha::obtenerDiaSemana();
    dia_semanal = Fecha::nombreDia(entero);

   if (larga)
   {
        if (conDia)
        {
            return dia_semanal + to_string(dia) + " de " + Fecha::nombreMes(mes) + " de " + to_string(anyo);
        }
        else
        {
            return to_string(dia) + " de " + Fecha::nombreMes(mes) + " de " + to_string(anyo);
        }
   }
   else
   {
        if (conDia)

        {
            
            return dia_semanal + to_string(dia) + "/" + to_string(mes) + "/" + to_string(anyo);
        }
        else
        {   
            
            return to_string(dia) + "/" + to_string(mes) + "/" + to_string(anyo);
        }

   }

}
