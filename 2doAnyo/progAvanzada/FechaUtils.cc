#include "FechaUtils.h"
#include <string>
#include <iostream>
using namespace std;

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
        case 0:
            return 0;
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

string FechaUtils::nombreMes(int mes)
{
    switch (mes)
    {
        case 1:
            return "Enero";
        case 2:
            return "Febrero";
        case 3:
            return "Marzo";
        case 4:
            return "Abril";
        case 5:
            return "Mayo";      
        case 6:
            return "Junio";
        case 7:
            return "Julio";
        case 8:
            return "Agosto";
        case 9:
            return "Septiembre";
        case 10:
            return "Octubre";
        case 11:
            return "Noviembre";
        case 12:
            return "Diciembre";
        default:
            return "Mes inválido";
    }
}

string FechaUtils::nombreDia(int dia, int mes, int anyo)
{
    // Día de referencia: 1 de enero de 2024 es un lunes
    int pivote_Lunes_1_enero_2024 = 0;
    int dias_transcurridos = 0;

    // Validar si la fecha es correcta
    if (compruebaFecha(dia, mes, anyo))
    {
        // Si el año es mayor o igual a 2024, ya tienes este código implementado correctamente
        if (anyo >= 2024) 
        {
            while (anyo >= 2024)
            {
                if (esBisiesto(anyo))
                {
                    for (int i = mes; i > 0; i--)
                    {
                        pivote_Lunes_1_enero_2024 += diasEnMesActual(i, true);
                    }
                } 
                else 
                {
                    for (int i = mes; i > 0; i--)
                    {
                        pivote_Lunes_1_enero_2024 += diasEnMesActual(i, false);
                    }
                }
                anyo--;
                mes = 12;
            }
            dia -= 1;
        } 
        else 
        {
            // Si el año es menor a 2024
            while (anyo < 2024)
            {
                if (esBisiesto(anyo))
                {
                    for (int i = mes; i <= 12; i++)
                    {
                        dias_transcurridos += diasEnMesActual(i, true);
                    }
                } 
                else 
                {
                    for (int i = mes; i <= 12; i++)
                    {
                        dias_transcurridos += diasEnMesActual(i, false);
                    }
                }
                anyo++;
                mes = 1; // Reiniciar al primer mes del siguiente año
                
            }

            // Ahora restamos los días acumulados desde el pivote (1 de enero de 2024)
            pivote_Lunes_1_enero_2024 -= dias_transcurridos;
        }



        // Determinar el día de la semana
        int diaSemana = (pivote_Lunes_1_enero_2024 + dia) % 7;
        if (diaSemana < 0) diaSemana += 7; // Asegurar que el resultado esté en el rango 0-6

        // Retornar el nombre del día de la semana
        switch (diaSemana)
        {
            case 0:
                return "Domingo";
            case 1:
                return "Lunes";
            case 2:
                return "Martes";
            case 3:
                return "Miércoles";
            case 4:
                return "Jueves";
            case 5:
                return "Viernes";
            case 6:
                return "Sábado";
        }
    }

    return "Fecha inválida"; // Si la fecha no es válida
}




