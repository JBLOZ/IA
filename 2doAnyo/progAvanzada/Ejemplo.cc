#include <iostream>
#include "Fecha.h"
#include <string>
using namespace std;


int main()
{
    Fecha fecha1 = Fecha();
    cout << "todo bien" << endl;
    Fecha fecha3 = Fecha(4,11,2020);

    cout << fecha1.aCadena(true,true) << endl;

    cout << fecha3.aCadena(true, true);


    
    return 0;
}
