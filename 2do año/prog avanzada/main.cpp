//
// Created by jordi on 12/09/2024.
//
#include <iostream>
using namespace std;

bool esBisiesto(int anyo) 
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

int diasEnMesActual(int mes, int bisiesto)
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


tuple<int, int, int> CalculaDia(int dia, int mes, int anyo, int incremento)
{
    int diaIncrementado = dia + incremento;
    bool bisiesto = esBisiesto(anyo);

    
    while (diaIncrementado > diasEnMesActual(mes, bisiesto)) 
    {
        diaIncrementado -= diasEnMesActual(mes, bisiesto);
        mes++;
        if (mes > 12) 
        {
            mes = 1;
            anyo++;
            bisiesto = esBisiesto(anyo);
        }
    }

    return {diaIncrementado, mes, anyo};
}

int main() {
    int dia,mes,anyo, incremento;
    cout << "Introduce el dia: ";
    cin >> dia;
    cout << "Introduce el mes: ";
    cin >> mes;
    cout << "Introduce el año: ";
    cin >> anyo;
    cout << "Introduce el incremento: ";
    cin >> incremento;

    auto nuevaFecha = CalculaDia(dia, mes, anyo, incremento);

    
    cout << get<0>(nuevaFecha) << "-" << get<1>(nuevaFecha) << "-" << get<2>(nuevaFecha) << endl;
    return 0;
}


