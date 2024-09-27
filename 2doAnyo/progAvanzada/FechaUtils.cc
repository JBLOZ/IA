#include "FechaUtils.h"

bool FechaUtils::esBisiesto(int anyo)
{
    if (anyo % 4 == 0)
    {
        if (anyo % 100 == 0)
        {
            if (anyo % 400 == 0)
            {
                return true;
            } else
            {
                return false;
            }
        } else {
            return true;
        }
    } else {
        return false;
    }
}

int FechaUtils::diasEnMesActual(int mes, bool bisiesto)
{
    switch (mes)
    {
        case 1:
        case 3:
        case 5:
        case 7:
        case 8:
        case 10:
        case 12:
            return 31;
        case 4:
        case 6:
        case 9:
        case 11:
            return 30;
        case 2:
            if (bisiesto)
            {
                return 29;
            } else
            {
                return 28;
            }
        default:
            return -1; // handle invalid month
    }
}

bool FechaUtils::compruebaFecha(int dia, int mes, int anyo)
{
    bool bisiesto = esBisiesto(anyo);
    int diasMes = diasEnMesActual(mes, bisiesto);
    if (diasMes == -1)
    {
        return false;
    }
    if (dia > diasMes || dia < 1)
    {
        return false;
    } 
    else
    {
        return true;
    }
}