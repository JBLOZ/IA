#ifndef FECHAUTILS_H
#define FECHAUTILS_H

#include <string>
using namespace std;

class FechaUtils {


    public:
    static bool esBisiesto(int anyo);
    static int diasEnMesActual(int mes, bool bisiesto);
    static bool compruebaFecha(int dia, int mes, int anyo);
    static string nombreMes(int mes);
    static string nombreDia(int dia, int mes, int anyo);

};

#endif