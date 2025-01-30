#include <iostream>
#include "Fecha.h"
#include <string>
#include "FechaUtils.h"
#include "evento.h"
using namespace std;



int main()
{
    Fecha fecha1 = Fecha();
    cout << "todo bien" << endl;
    Fecha fecha3 = Fecha(2,2,2024);
    Fecha fecha4 = Fecha(30,12,2023);
    cout << fecha3.aCadena(true, true);
    cout << fecha4.aCadena();
    fecha4.incrementaAnyos(4);
    cout << fecha4.aCadena();
    cout << FechaUtils::nombreMes(12);
    Evento evento1(fecha3);


    
    return 0;
}



