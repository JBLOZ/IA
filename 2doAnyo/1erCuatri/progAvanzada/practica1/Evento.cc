#include "Evento.h"
#include "Fecha.h"
#include <string>
#include <iostream>
using namespace std;



Evento::Evento()
{
    this->fecha = Fecha(1,1,1900);
    this->descripcion = "sin descripcion";
    cout << this->fecha.aCadena();
}


Evento::Evento(const Fecha& fecha, string descripcion)
{
    this->fecha = fecha;    
    this->descripcion = descripcion;
}

Evento::~Evento()
{


}


