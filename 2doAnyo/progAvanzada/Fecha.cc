#include "Fecha.h"
#include <iostream>
#include "FechaUtils.h"
using namespace std;



Fecha::Fecha()
{   
    cout << "clase fecha construida" << endl;
    dia = 1;
    mes = 1;
    anyo = 1900;
}

Fecha::~Fecha()
{
    cout << "clase fecha destruida" << endl;
    dia = 1;
    mes = 1;
    anyo = 1900;
}

Fecha::Fecha(int dia, int mes, int anyo)
{
    cout << "clase fecha construida con parametros" << endl;
    if (FechaUtils::compruebaFecha(dia, mes, anyo))
    {
        cout << dia << mes << anyo;
    } 
    else
    {   
        cout << "fecha incorrecta" << endl;
        *this = Fecha();
    }
}

Fecha::Fecha(const Fecha& other)
{
    cout << "clase fecha copiada" << endl;
    this->dia = other.dia;
    this->mes = other.mes;
    this->anyo = other.anyo;
}

Fecha& Fecha::operator=(const Fecha &other)
{
    if (this != &other) {
        this->dia = other.dia;
        this->mes = other.mes;
        this->anyo = other.anyo;
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

bool Fecha::setDia(int)
{
    return true;
}

string Fecha::aCadena(bool larga, bool conDia) const
{
    string cadena = "";
    if (conDia)
    {
        cadena += to_string(dia);
    }  
    cadena += "/" + to_string(mes) + "/" + to_string(anyo);

    cout << cadena;
}
