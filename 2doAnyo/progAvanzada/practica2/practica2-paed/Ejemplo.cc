#include "Calendario.h"
#include <iostream>
using namespace std;

// void testStr( const string& name ,const string& output, const string& expected){
//     cout << name << ": ";
//     if( output == expected ){
//         cout << "OK" << endl;
//     }else{
//         cout << "ERROR: se esperaba:'"<<expected<<"' pero la salida ha sido:'"<<output<<"'"<< endl;
//     }
// }

// void testBool(const string& name, bool output, bool expected){
//     cout << name << ": ";
//     if( output == expected ){
//         cout << "OK" << endl;
//     }else{
//         cout << "ERROR: se esperaba:'"<<expected<<"' pero la salida ha sido:'"<<output<<"'"<< endl;
//     }
// }

int main(){
    Calendario c;

    

    Fecha f2(3,5,2000);
    Evento ev(f2," ");
    Fecha f1(1,2,2017);
    cout << c.aCadena() << endl;
    cout << c.comprobarEvento(f2) << endl;
    




    // testStr("aCadena 1",c.aCadena(),"");

    // //Inserción de 3 eventos
    // Fecha f(9,9,2024);
    // testBool("Insertar 1",c.insertarEvento(f,"Inicio del curso 2024/2025"),true);

    // f.setDia(23);
    // f.setMes(5);
    // f.setAnyo(2025);
    // testBool("Insertar 2",c.insertarEvento(f,"Final del curso 2024/2025"),true);

    // f.setDia(24);
    // f.setMes(5);
    // f.setAnyo(2024);
    // testBool("Insertar 3",c.insertarEvento(f,"Final del curso 2023/2024"),true);

    // f.setDia(11);
    // f.setMes(9);
    // f.setAnyo(2023);
    // testBool("Insertar 4",c.insertarEvento(f,"Inicio del curso 2023/2024"),true);

    // testBool("Comprobar 1", c.comprobarEvento(f), true);

    // //No debe haber un evento
    // f.incrementaAnyos(1);
    // testBool("Comprobar 2", c.comprobarEvento(f), false);

    // //No hace nada
    // testBool("Eliminar 1", c.eliminarEvento(f), false);

    // //Cadena vacía
    // testStr("Descripción 1",c.obtenerDescripcion(f),"");

    // f.setDia(24);
    // f.setMes(5);
    // f.setAnyo(2024);
    // //"Final del curso 2023/2024"
    // testStr("Descripción 2",c.obtenerDescripcion(f),"Final del curso 2023/2024");

    // //Elimina evento
    // testBool("Eliminar 2", c.eliminarEvento(f), true);

    // testStr("Descripción 3",c.obtenerDescripcion(f),"");

    // string tresEventos="lunes 11 de septiembre de 2023:Inicio del curso 2023/2024\nlunes 9 de septiembre de 2024:Inicio del curso 2024/2025\nviernes 23 de mayo de 2025:Final del curso 2024/2025\n";
    // testStr("aCadena2",c.aCadena(),tresEventos);

    // int total=0;
    // for(IteradorCalendario it=c.begin(); it != c.end(); it.step()){
    //     total++;
    // }
    // testBool("Iterador 1",total==3,true);

    // IteradorCalendario it=c.begin();
    // testStr("getEvento 1",c.getEvento(it).getDescripcion(),"Inicio del curso 2023/2024");
    // it.step();
    // testStr("getEvento 2",c.getEvento(it).getDescripcion(),"Inicio del curso 2024/2025");
    // it.step();
    // testStr("getEvento 3",c.getEvento(it).getDescripcion(),"Final del curso 2024/2025");

    // //No hace nada
    // c.importarEventos(c);

    // testStr("aCadena2",c.aCadena(),tresEventos);

    // Calendario c2(c);
    // Fecha f2(1,1,2026);
    // testBool("Insertar 5",c2.insertarEvento(f2,"Concierto de año nuevo"),true);

    // c.importarEventos(c2);

    // string cuatroEventos=tresEventos+"jueves 1 de enero de 2026:Concierto de año nuevo\n";
    
    // testStr("aCadena4",c.aCadena(),cuatroEventos);


}