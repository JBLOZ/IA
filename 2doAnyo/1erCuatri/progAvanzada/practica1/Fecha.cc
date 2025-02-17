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

}

Fecha::Fecha(int dia, int mes, int anyo)
{
    cout << "clase fecha construida con parametros" << endl;
    if (FechaUtils::compruebaFecha(dia, mes, anyo))
    {
        this->dia = dia;
        this->mes = mes;
        this->anyo = anyo;
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

bool Fecha::setDia(int nuevoDia)
{
    if (FechaUtils::compruebaFecha(nuevoDia, this->mes, this->anyo))
    {
        this->dia = nuevoDia;
        return true;
    }
    return false;
}

bool Fecha::setMes(int nuevoMes)
{
    if (FechaUtils::compruebaFecha(this->dia, nuevoMes, this->anyo))
    {
        this->mes = nuevoMes;
        return true;
    }
    return false;
}

bool Fecha::setAnyo(int nuevoAnyo)
{
    if (FechaUtils::compruebaFecha(this->dia, this->mes, nuevoAnyo))
    {
        this->anyo = nuevoAnyo;
        return true;
    }
    return false;
}

string Fecha::aCadena(bool larga, bool conDia) {
    string cadena = "";

    if (conDia)
    {
        if (larga)
        {
            cadena += FechaUtils::nombreDia(dia, mes, anyo) + " " + to_string(dia) + " de " + FechaUtils::nombreMes(mes) + " de " + to_string(anyo);
        }
        else
        {
            cadena += to_string(dia) + "/" + to_string(mes) + "/" + to_string(anyo);
        }
    }
    else
    {
        if (larga)
        {
            cadena += FechaUtils::nombreMes(mes) + " de " + to_string(anyo);
        }
        else
        {
            cadena += to_string(mes) + "/" + to_string(anyo);
        }
    }
    return cadena + "\n";
}

bool Fecha::incrementaDias(int dias)
{
    int nuevoDia = this->dia + dias;
    int nuevoMes = this->mes;
    int nuevoAnyo = this->anyo;

    while (nuevoDia > FechaUtils::diasEnMesActual(nuevoMes, FechaUtils::esBisiesto(nuevoAnyo)))
    {
        nuevoDia -= FechaUtils::diasEnMesActual(nuevoMes, FechaUtils::esBisiesto(nuevoAnyo));
        nuevoMes++;
        if (nuevoMes > 12)
        {
            nuevoMes = 1;
            nuevoAnyo++;
        }
    }

    if (FechaUtils::compruebaFecha(nuevoDia, nuevoMes, nuevoAnyo))
    {
        this->dia = nuevoDia;
        this->mes = nuevoMes;
        this->anyo = nuevoAnyo;
        return true;
    }
    return false;
}


bool Fecha::incrementaMeses(int meses)
{
    int nuevoMes = this->mes + meses;
    int nuevoAnyo = this->anyo;

    while (nuevoMes > 12)
    {
        nuevoMes -= 12;
        nuevoAnyo++;
    }

    if (FechaUtils::compruebaFecha(this->dia, nuevoMes, nuevoAnyo))
    {
        this->mes = nuevoMes;
        this->anyo = nuevoAnyo;
        return true;
    }

    return false;
}

bool Fecha::incrementaAnyos(int anyos)
{
    int nuevoAnyo = this->anyo + anyos;

    if (FechaUtils::compruebaFecha(this->dia, this->mes, nuevoAnyo))
    {
        this->anyo = nuevoAnyo;
        return true;
    }

    return false;
}   
