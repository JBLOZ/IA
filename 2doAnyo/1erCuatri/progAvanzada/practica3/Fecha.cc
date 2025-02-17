#include "Fecha.h"
#include <iostream>
using namespace std;

bool Fecha::esFechaCorrecta(int d,int m,int a) const {
    if(a<1900 || m<1 || m>12 || d<1) return false;
    return (d<=calculaDiasMes(m,a));
}

bool Fecha::esBisiesto(int a) const {
    return ((a%4==0 && a%100!=0) || (a%400==0));
}

int Fecha::calculaDiasMes(int m, int a) const {
    switch (m){
        case 1:case 3:case 5:case 7:case 8:case 10:case 12:return 31;
        case 4:case 6:case 9:case 11:return 30;
        case 2:return (esBisiesto(a)?29:28);
    }
    return -1;
}

string Fecha::nombreMes(int m) const {
    string meses[12]={"enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"};
    if(m<1||m>12) return "mes incorrecto";
    return meses[m-1];
}

string Fecha::nombreDia(int d) const {
    // d: 0=lunes,1=martes,...6=domingo
    string dias[7]={"lunes","martes","miércoles","jueves","viernes","sábado","domingo"};
    if(d<0||d>6) return "día incorrecto";
    return dias[d];
}

int Fecha::obtenerDiaSemana() const {
    int d = dia;
    int m = mes;
    int y = anyo;

    // Si el mes es enero o febrero, se considera como el mes 13 y 14 del año anterior
    if(m < 3) {
        m += 12;
        y -= 1;
    }

    int K = y % 100;
    int J = y / 100;

    // Fórmula de Zeller
    int f = d + (13*(m+1))/5 + K + K/4 + J/4 + 5*J;
    f = f % 7; 

    // Ahora f=0 representa sábado
    // Queremos 0=lunes,1=martes,...,6=domingo
    // Mapeo actual (f=0 sabado):
    // f:0=sat,1=sun,2=mon,3=tue,4=wed,5=thu,6=fri
    // Queremos:0=lun,1=mar,2=mié,3=jue,4=vie,5=sáb,6=dom
    // Observando el patrón:
    // mon(2 zeller) -> 0 nuestro
    // Para alinear: nuevo_indice = (f + 5) % 7 (tal como estaba antes)
    // Comprobamos: f=0(sat) -> (0+5)%7=5=sábado (correcto)
    // f=1(sun) -> (1+5)%7=6=domingo (correcto)
    // f=2(mon) -> (2+5)%7=0=lunes (correcto)
    // y así sucesivamente.

    return (f+5)%7;
}

Fecha::Fecha(){
    dia=1;mes=1;anyo=1900;
}

Fecha::Fecha(int d,int m,int a){
    if(esFechaCorrecta(d,m,a)) {
        dia=d;mes=m;anyo=a;
    } else {
        dia=1;mes=1;anyo=1900;
    }
}

Fecha::Fecha(const Fecha &f){
    if(esFechaCorrecta(f.dia,f.mes,f.anyo)) {
        dia=f.dia;mes=f.mes;anyo=f.anyo;
    } else {
        dia=1;mes=1;anyo=1900;
    }
}

Fecha::~Fecha(){
    dia=1;mes=1;anyo=1900;
}

Fecha& Fecha::operator=(const Fecha &f){
    if(this!=&f){
        if(esFechaCorrecta(f.dia,f.mes,f.anyo)) {
            dia=f.dia;mes=f.mes;anyo=f.anyo;
        } else {
            dia=1;mes=1;anyo=1900;
        }
    }
    return *this;
}

int Fecha::getDia() const {return dia;}
int Fecha::getMes() const {return mes;}
int Fecha::getAnyo() const{return anyo;}

bool Fecha::setDia(int d) {
    if(esFechaCorrecta(d,mes,anyo)){dia=d;return true;}
    return false;
}
bool Fecha::setMes(int m) {
    if(esFechaCorrecta(dia,m,anyo)){mes=m;return true;}
    return false;
}
bool Fecha::setAnyo(int a) {
    if(esFechaCorrecta(dia,mes,a)){anyo=a;return true;}
    return false;
}

bool Fecha::operator==(const Fecha &f) const {
    return (dia==f.dia && mes==f.mes && anyo==f.anyo);
}
bool Fecha::operator!=(const Fecha &f) const {
    return !(*this==f);
}
bool Fecha::operator<(const Fecha &f) const {
    if(anyo<f.anyo) return true;
    if(anyo>f.anyo) return false;
    if(mes<f.mes) return true;
    if(mes>f.mes) return false;
    return (dia<f.dia);
}
bool Fecha::operator>(const Fecha &f) const {
    return f<*this;
}

// Zeller’s congruence (modificación para días del 0 al 6)
// 0=Saturday, 1=Sunday, 2=Monday, ..., 6=Friday.


bool Fecha::incrementaDias(int inc) {
    // Convertir fecha a días desde 1/1/1900
    int totalDays = 0;
    // Contamos años completos
    for (int year=1900; year<anyo; year++) {
        totalDays += (esBisiesto(year)?366:365);
    }
    // Añadimos meses del año actual
    for (int mm=1; mm<mes; mm++) {
        totalDays += calculaDiasMes(mm, anyo);
    }
    // Añadimos los días del mes actual (dia-1 porque el 1 de enero de 1900 sería día 0)
    totalDays += (dia-1);

    // Incrementamos
    totalDays += inc;
    if (totalDays<0) {
        // No soportamos fechas antes de 1/1/1900 en este caso, puedes decidir qué hacer
        return false;
    }

    // Convertir de vuelta a fecha
    int yy=1900;
    while (true) {
        int dyear = esBisiesto(yy)?366:365;
        if (totalDays < dyear) break;
        totalDays -= dyear;
        yy++;
    }

    int mm=1;
    while (true) {
        int dmes = calculaDiasMes(mm, yy);
        if (totalDays < dmes) break;
        totalDays -= dmes;
        mm++;
    }

    int dd = totalDays + 1; // sumamos 1 porque empezamos en 0
    if (!esFechaCorrecta(dd, mm, yy)) return false;
    dia=dd; mes=mm; anyo=yy;
    return true;
}


bool Fecha::incrementaMeses(int inc) {
    int mm=mes+inc;int aa=anyo;int dd=dia;
    while(mm>12){mm-=12;aa++;}
    while(mm<1){mm+=12;aa--;}
    if(dd>calculaDiasMes(mm,aa)) return false;
    mes=mm;anyo=aa;dia=dd;return true;
}

bool Fecha::incrementaAnyos(int inc){
    int yy=anyo+inc;
    if(!esFechaCorrecta(dia,mes,yy)) return false;
    anyo=yy;return true;
}

string Fecha::aCadena(bool larga, bool conDia) const {
    if(larga){
        // formato largo conDia = true: "lunes 9 de septiembre de 2024"
        // conDia = false: "9 de septiembre de 2024"
        if(conDia){
            return nombreDia(obtenerDiaSemana())+" "+to_string(dia)+" de "+nombreMes(mes)+" de "+to_string(anyo);
        } else {
            return to_string(dia)+" de "+nombreMes(mes)+" de "+to_string(anyo);
        }
    } else {
        // formato corto conDia = true: "lunes 9/9/2024"
        // conDia = false: "9/9/2024"
        if(conDia){
            return nombreDia(obtenerDiaSemana())+" "+to_string(dia)+"/"+to_string(mes)+"/"+to_string(anyo);
        } else {
            return to_string(dia)+"/"+to_string(mes)+"/"+to_string(anyo);
        }
    }
}
