#include "Calendario.h"
#include <iostream>
using namespace std;

void testStr( const string& name ,const string& output, const string& expected){
    cout << name << ": ";
    if( output == expected ){
        cout << "OK" << endl;
    }else{
        cout << "ERROR: se esperaba:'"<<expected<<"' pero la salida ha sido:'"<<output<<"'"<< endl;
    }
}

void testBool(const string& name, bool output, bool expected){
    
}

int main() {
    // Tu código aquí

    cout << "hola";
    return 0;
}
