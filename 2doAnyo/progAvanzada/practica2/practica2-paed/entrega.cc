#ifndef FECHA_H
#define FECHA_H

#include <string>

using namespace std;

class Fecha{
   private:

   int dia, mes, anyo;
   //Puede ser útil: eliminar si no se han implementado estos métodos auxiliares
   bool esFechaCorrecta(int, int, int) const;
   bool esBisiesto(int) const ;
   int calculaDiasMes(int, int) const;
   int obtenerDiaSemana() const;


   public:
   
   //Constructor por defecto: inicializa la fecha a 1/1/1900
   Fecha();
   
   //Constructor sobrecargado: inicializa la fecha según los parámetros
   Fecha(int dia,int mes,int anyo);
   
   //Constructor de copia
   Fecha(const Fecha &);

   string nombreMes(int m) const;
   string nombreDia(int d) const;
   
   //Destructor: pone la fecha a 1/1/1900
   ~Fecha();

   //Operador de asignación
   Fecha& operator=(const Fecha &);
   
   //Operador de comparación
   bool operator==(const Fecha &) const;
   
   //Operador de comparación
   bool operator!=(const Fecha &) const;
   
   //Operador de comparación
   bool operator<(const Fecha &) const;
   
   //Operador de comparación
   bool operator>(const Fecha &) const;
   
   
   //Devuelve el día
   int getDia() const;
   
   //Devuelve el mes
   int getMes() const;
   
   //Devuelve el año
   int getAnyo() const;
   
   //Modifica el día: devuelve false si la fecha resultante es incorrecta
   bool setDia(int);
   
   //Modifica el mes: devuelve false si la fecha resultante es incorrecta
   bool setMes(int);

  //Modifica el anyo: devuelve false si la fecha resultante es incorrecta
   bool setAnyo(int);

  //Incrementa la fecha en el número de días pasado como parámetro.
  //Si el parámetro es negativo, la decrementa
  bool incrementaDias(int );
  
  //Incrementa la fecha en el número de meses pasado como parámetro.
  //Si el parámetro es negativo, la decrementa
  bool incrementaMeses(int );
 
  //Incrementa la fecha en el número de años pasado como parámetro.
  //Si el parámetro es negativo, la decrementa
  bool incrementaAnyos(int );
  
  //Devuelve una representación como cadena de la fecha
  string aCadena(bool larga, bool conDia) const;
   
};

#endif

#ifndef EVENTO_H
#define EVENTO_H

#include<string>
using namespace std;

class Evento{
private:

Fecha fecha;
string descripcion;

public:
//Constructor por defecto: inicializa la fecha a 1/1/1900 ... 
//y la descripción a "sin descripción"
Evento();
//Constructor sobrecargado: inicializa la fecha según los parámetros
Evento(const Fecha&, const string&);
//Constructor de copia
Evento(const Evento&);
//Operador de asignación
Evento& operator=(const Evento &);
//Destructor: pone la fecha a 1/1/1900 y la descripción a "sin descripción"
~Evento();
//Operador de comparación
bool operator==(const Evento &) const;
//Operador de comparación
bool operator!=(const Evento &) const;
//Operador de comparación
bool operator<(const Evento &) const;
//Operador de comparación
bool operator>(const Evento &) const;
//Devuelve (una copia de) la fecha
Fecha getFecha() const;
//Devuelve (una copia de) la descripción
string getDescripcion() const;
//Modifica la fecha
void setFecha(const Fecha& );
//Modifica la descripción
bool setDescripcion(const string &);

};
#endif

#ifndef CALENDARIO_H
#define CALENDARIO_H


using namespace std;

class NodoCalendario{
private:
    NodoCalendario* siguiente;
    Evento evento;

public:
    // Constructor por defecto
    NodoCalendario();   
    // Constructor sobrecargado
    NodoCalendario(NodoCalendario*, const Evento&);
    // Constructor de copia
    NodoCalendario(const NodoCalendario&);
    // Operador de asignación
    NodoCalendario& operator=(const NodoCalendario&);
    // Destructor
    ~NodoCalendario();
    // Devuelve el puntero al siguiente nodo de la lista
    NodoCalendario* getSiguiente() const;
    // Devuelve el evento almacenado en el nodo
    Evento getEvento() const;
    // Modifica el puntero al siguiente nodo de la lista
    void setSiguiente(NodoCalendario*);
    // Modifica el evento
    void setEvento(const Evento&);
};

class IteradorCalendario{
private:
    NodoCalendario* pt;

public:
    // Constructor por defecto: puntero a nullptr
    IteradorCalendario();
    // Constructor de copia
    IteradorCalendario(const IteradorCalendario&);
    // Destructor: puntero a nullptr
    ~IteradorCalendario();
    // Operador de asignación
    IteradorCalendario& operator=(const IteradorCalendario&);
    // Incrementa el iterador en un paso
    void step();
    // Operador de comparación
    bool operator==(const IteradorCalendario&) const;
    // Operador de comparación
    bool operator!=(const IteradorCalendario&) const;

    friend class Calendario;
};

class Calendario{
private:
    NodoCalendario* head;

public:
    // Constructor por defecto: calendario sin ningún evento
    Calendario();
    // Constructor de copia
    Calendario(const Calendario&);
    // Operador de asignación
    Calendario& operator=(const Calendario&);
    // Destructor
    ~Calendario();
    // Devuelve un iterador al comienzo del calendario
    IteradorCalendario begin() const;
    // Devuelve un iterador al final del calendario: puntero a nullptr
    IteradorCalendario end() const;
    // Devuelve el evento apuntado por el iterador
    Evento getEvento(const IteradorCalendario& it) const;
    // Añade un evento al calendario
    bool insertarEvento(const Fecha&, const string&);
    // Elimina un evento del calendario
    bool eliminarEvento(const Fecha&);
    // Comprueba si hay algún evento asociado a la fecha dada
    bool comprobarEvento(const Fecha&) const;
    // Obtiene la descripción asociada al evento
    string obtenerDescripcion(const Fecha&) const;
    // Añade todos los eventos del calendario pasado como parámetro
    void importarEventos(const Calendario&);
    // Devuelve una cadena con el contenido completo del calendario
    string aCadena() const;
};

#endif



#include<iostream>
#include<string>
using namespace std;

int main(){

  Calendario c;
  
  int d,m,a;
  string desc, sep;
  char car;
  
  cin >> d;
  while( d > 0){
    cin >> m;
    cin >> a;
    Fecha f(d,m,a);
    cin >> sep;
    
    cin.get(car);
    
    getline(cin,desc);
    
    c.insertarEvento(f,desc);
   
    cin >> d;
  }
  
  cout << c.aCadena()<< endl;

  return 0;

}

#include<string>
#include <iostream>
using namespace std;


/*
Métodos privados
Si decides implementar los métodos privados que se proponen en el fichero Fecha.h,
puedes hacerlo aquí.

Asegúrate de añadir el código correspondiente en el interior de cada método
*/


bool Fecha::esFechaCorrecta(int dia,int mes,int anyo) const
{
    if (anyo>=1900 && mes>=1 && mes<=12 && dia>=1)
    {
        if (dia <= Fecha::calculaDiasMes(mes, anyo))
        {   
            
            return true;
        }
    }
    return false;
}



bool Fecha::esBisiesto(int a) const
{
    return (a%4==0 && (a%100 !=0 || a%400== 0));
}



int Fecha::calculaDiasMes(int m, int a) const{
    switch (m)
    {
        case 1:
        case 3:
        case 5:
        case 7:
        case 8:
        case 10:
        case 12:
        return 31;
        case 2:
        if (Fecha::esBisiesto(a)) {return 29;}
        else {return 28;}
        case 4:
        case 6:
        case 9:
        case 11:
        return 30;
        default:
        return -1;
    }
}


string Fecha::nombreMes(int m) const
{
    switch (m)
    {
    case 1:
    return "enero";
    case 2:
    return "febrero";
    case 3:
    return "marzo";
    case 4:
    return "abril";
    case 5:
    return "mayo";
    case 6:
    return "junio";
    case 7:
    return "julio";
    case 8:
    return "agosto";
    case 9:
    return "septiembre";
    case 10:
    return "octubre";
    case 11:
    return "noviembre";
    case 12:
    return "diciembre";
    default:
    return "mes incorrecto";
        
    }
}
string Fecha::nombreDia(int d) const
{
    switch (d)
    {
        case 0:
        return "lunes ";
        break;
        case 1:
        return "martes ";
        break;
        case 2:
        return "miércoles ";
        break;
        case 3:
        return "jueves ";
        break;
        case 4:
        return "viernes ";
        break;
        case 5:
        return "sabado ";
        break;
        case 6: 
        return "domingo ";
        break;
        default:
        return "dia incorrecto";
    }
}


int Fecha::obtenerDiaSemana() const 
{
    int d = this->getDia();
    int m = this->getMes();
    int y = this->getAnyo();
    int f;

    if (m < 3) 
    {
        m += 12;
        y -= 1;
    }

    int K = y % 100;
    int J = y / 100;


    f = d + (13 * (m + 1) / 5) + K + (K / 4) + (J / 4) - 2 * J;
    f = (f + 5) % 7;

    return f;
}

/*
Métodos públicos
*/
Fecha::Fecha(){
    dia = 1;
    mes = 1;
    anyo = 1900;
}

Fecha::Fecha(int d,int m,int a){
    if (Fecha::esFechaCorrecta(d,m,a))
    {
        dia = d;
        mes = m;
        anyo = a;
    }
    else
    {
        dia = 1;
        mes = 1;
        anyo = 1900;
    }
}

Fecha::Fecha(const Fecha &f){
    if (Fecha::esFechaCorrecta(f.dia,f.mes,f.anyo))
    {
        dia = f.dia;
        mes = f.mes;
        anyo = f.anyo;
    }
    else
    {
        dia = 1;
        mes = 1;
        anyo = 1900;
    }
}


Fecha::~Fecha(){
    dia = 1;
    mes = 1;
    anyo = 1900;
}

Fecha& Fecha::operator=(const Fecha &f){
    if (Fecha::esFechaCorrecta(f.dia,f.mes,f.anyo))
    {
        this->dia = f.dia;
        this->mes = f.mes;
        this->anyo = f.anyo;
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


bool Fecha::setDia(int d)
{
    if (Fecha::esFechaCorrecta(d,mes,anyo))
    {
        dia = d;
        return true;
    }
    return false;
}

bool Fecha::setMes(int m){

    if (Fecha::esFechaCorrecta(dia,m,anyo))
    {
        mes = m;
        return true;
    }
    return false;
}

bool Fecha::setAnyo(int a){
   if (Fecha::esFechaCorrecta(dia,mes,a))
   {
        anyo = a;
        return true;
   }
    return false;
}


bool Fecha::operator==(const Fecha &f) const
{
    if (f.dia == this->dia && f.mes == this->mes && f.anyo == this->anyo)
    {
        return true;
    }
    else 
    {
        return false;
    }

}

bool Fecha::operator!=(const Fecha &f) const
{
    if (f.dia != this->dia || f.mes != this->mes || f.anyo != this->anyo)
    {
        return true;
    }
    else
    {
        return false;
    }
}
      


bool Fecha::operator<(const Fecha &f) const 
{
    if (this->anyo < f.getAnyo()) 
    {
        return true;
    } 
    else if (this->anyo == f.getAnyo()) 
    {
        if (this->mes < f.mes) 
        {
            return true;
        } 
        else if (this->mes == f.mes) 
        {
            return this->dia < f.dia;
        }
    }
    return false;
}

bool Fecha::operator>(const Fecha &f) const 
{
    if (this->anyo > f.getAnyo()) 
    {
        return true;
    } 
    else if (this->anyo == f.getAnyo()) 
    {
        if (this->mes > f.mes) 
        {
            return true;
        } 
        else if (this->mes == f.mes) 
        {
            return this->dia > f.dia;
        }
    }
    return false;
}




bool Fecha::incrementaDias(int inc)
{
    int dias_incremento, copia_dia, copia_mes, copia_anyo;
    copia_dia = dia;
    copia_mes = mes;
    copia_anyo = anyo;
    dias_incremento = dia + inc;
    if (inc > 0)
    {
        
        while (dias_incremento > Fecha::calculaDiasMes(mes,anyo))
        {
            dias_incremento -= Fecha::calculaDiasMes(mes,anyo);
            if (mes == 12)
            {
                mes = 1;
                anyo += 1;
            }
            else
            {
                mes += 1;
            }
        }
        
    }
    else if (inc<0)
    {
        while (dias_incremento <= 0)
        {
            if (mes == 1)
            {
                mes = 12;
                anyo -=1;
            }
            else
            {
                mes -= 1;
            }
            dias_incremento += Fecha::calculaDiasMes(mes,anyo);
        }
        
    }
    dia = dias_incremento;
    if (Fecha::esFechaCorrecta(dia,mes,anyo))
    {
        return true;
    }
    else
    {
        dia = copia_dia;
        mes = copia_mes;
        anyo = copia_anyo;
        return false;


    }

}


bool Fecha::incrementaMeses(int inc)
{
    if (Fecha::esFechaCorrecta(dia,mes+inc,anyo))
    {
        mes += inc;
        return true;
    }

    return false;
}

bool Fecha::incrementaAnyos(int inc)
{
    if (Fecha::esFechaCorrecta(dia,mes,anyo+inc))
    {
        anyo += inc;
        return true;
    }

    return false;
}


string Fecha::aCadena(bool larga, bool conDia) const
{

   string cadena, dia_semanal;
   int entero;
   entero = Fecha::obtenerDiaSemana();
    dia_semanal = Fecha::nombreDia(entero);

   if (larga)
   {
        if (conDia)
        {
            return dia_semanal + to_string(dia) + " de " + Fecha::nombreMes(mes) + " de " + to_string(anyo);
        }
        else
        {
            return to_string(dia) + " de " + Fecha::nombreMes(mes) + " de " + to_string(anyo);
        }
   }
   else
   {
        if (conDia)

        {
            
            return dia_semanal + to_string(dia) + "/" + to_string(mes) + "/" + to_string(anyo);
        }
        else
        {   
            
            return to_string(dia) + "/" + to_string(mes) + "/" + to_string(anyo);
        }

   }

}



Evento::Evento()
{
    this->descripcion = "sin descripción";
}

Evento::Evento(const Fecha& f, const string& d){

    this->fecha = f;
    if (d=="")
    {
        this->descripcion = "sin descripción";
    }
    else
    {
        this->descripcion = d;
    }
    

}

Evento::Evento(const Evento& e){
    this->fecha = e.fecha;
    this->descripcion = e.descripcion;

}

Evento& Evento::operator=(const Evento &e){
    if (this != &e)
    { 
        this->fecha = e.fecha;
        this->descripcion = e.descripcion;
    }
    return *this;
}

Evento::~Evento(){

    this->fecha = Fecha();
    this->descripcion = "sin descripción";

}

//Operador de comparación
bool Evento::operator==(const Evento &e) const{

    return (this->fecha == e.fecha and this->descripcion == e.descripcion);

}

//Operador de comparación
bool Evento::operator!=(const Evento &e) const{
    return(this->fecha != e.fecha || this->descripcion != e.descripcion);
}
//Operador de comparación
bool Evento::operator<(const Evento &e) const{
    return (this->fecha < e.fecha);
}

//Operador de comparación
bool Evento::operator>(const Evento &e) const{
    return(this->fecha > e.fecha);
}

//Devuelve (una copia de) la fecha
Fecha Evento::getFecha() const{
    
    return this->fecha;
}

//Devuelve (una copia de) la descripción
string Evento::getDescripcion() const{

    return this->descripcion;
}

//Modifica la fecha
void Evento::setFecha(const Fecha& f){
    this->fecha = f;
}

//Modifica la descripción
bool Evento::setDescripcion(const string &d){   
    if(d == "")
    {
        this->descripcion = "sin descripción";
    }
    else
    {
        this->descripcion = d;
    }
    return true;
}


/*** NodoCalendario ***/

// Constructor por defecto
NodoCalendario::NodoCalendario() {
    siguiente = nullptr;
  
}

// Constructor sobrecargado
NodoCalendario::NodoCalendario(NodoCalendario* s, const Evento& e) {
    siguiente = s;
    evento = e;
}

// Constructor de copia
NodoCalendario::NodoCalendario(const NodoCalendario& nc) {
    siguiente = nc.siguiente;
    evento = nc.evento;
}

// Operador de asignación
NodoCalendario& NodoCalendario::operator=(const NodoCalendario& nc) {
    if (this != &nc) {
        siguiente = nc.siguiente;
        evento = nc.evento;
    }
    return *this;
}

// Destructor
NodoCalendario::~NodoCalendario() {
    // No se libera memoria aquí; se maneja desde Calendario
    siguiente = nullptr;
}

// Devuelve el puntero al siguiente nodo de la lista
NodoCalendario* NodoCalendario::getSiguiente() const {
    return siguiente;
}

// Devuelve el evento almacenado en el nodo
Evento NodoCalendario::getEvento() const {
    return evento;
}

// Modifica el puntero al siguiente nodo de la lista
void NodoCalendario::setSiguiente(NodoCalendario* s) {
    siguiente = s;
}

// Modifica el evento
void NodoCalendario::setEvento(const Evento& e) {
    evento = e;
}

/*** IteradorCalendario ***/

// Constructor por defecto: puntero a nullptr
IteradorCalendario::IteradorCalendario() {
    pt = nullptr;
}

// Constructor de copia
IteradorCalendario::IteradorCalendario(const IteradorCalendario& ic) {
    pt = ic.pt;
}

// Destructor: puntero a nullptr
IteradorCalendario::~IteradorCalendario() {
    pt = nullptr;
}

// Operador de asignación
IteradorCalendario& IteradorCalendario::operator=(const IteradorCalendario& ic) {
    if (this != &ic) {
        pt = ic.pt;
    }
    return *this;
}

// Incrementa el iterador en un paso
void IteradorCalendario::step() {
    if (pt != nullptr) {
        pt = pt->getSiguiente();
    }
}

// Operador de comparación
bool IteradorCalendario::operator==(const IteradorCalendario& ic) const {
    return pt == ic.pt;
}

// Operador de comparación
bool IteradorCalendario::operator!=(const IteradorCalendario& ic) const {
    return pt != ic.pt;
}

/*** Calendario ***/

// Constructor por defecto: calendario sin ningún evento
Calendario::Calendario() {
    head = nullptr;
}

// Constructor de copia
Calendario::Calendario(const Calendario& c) {
    head = nullptr;
    NodoCalendario* actual = c.head;
    NodoCalendario* previo = nullptr;

    while (actual != nullptr) {
        NodoCalendario* nuevoNodo = new NodoCalendario();
        nuevoNodo->setEvento(actual->getEvento());
        nuevoNodo->setSiguiente(nullptr);

        if (head == nullptr) {
            head = nuevoNodo;
        } else {
            previo->setSiguiente(nuevoNodo);
        }

        previo = nuevoNodo;
        actual = actual->getSiguiente();
    }
}

// Operador de asignación
Calendario& Calendario::operator=(const Calendario& c) {
    if (this != &c) {
        // Liberar la lista actual
        NodoCalendario* actual = head;
        while (actual != nullptr) {
            NodoCalendario* temp = actual;
            actual = actual->getSiguiente();
            delete temp;
        }
        head = nullptr;

        // Copiar desde c
        actual = c.head;
        NodoCalendario* previo = nullptr;

        while (actual != nullptr) {
            NodoCalendario* nuevoNodo = new NodoCalendario();
            nuevoNodo->setEvento(actual->getEvento());
            nuevoNodo->setSiguiente(nullptr);

            if (head == nullptr) {
                head = nuevoNodo;
            } else {
                previo->setSiguiente(nuevoNodo);
            }

            previo = nuevoNodo;
            actual = actual->getSiguiente();
        }
    }
    return *this;
}

// Destructor
Calendario::~Calendario() {
    NodoCalendario* actual = head;
    while (actual != nullptr) {
        NodoCalendario* temp = actual;
        actual = actual->getSiguiente();
        delete temp;
    }
    head = nullptr;
}

// Devuelve un iterador al comienzo del calendario
IteradorCalendario Calendario::begin() const {
    IteradorCalendario it;
    it.pt = head;
    return it;
}

// Devuelve un iterador al final del calendario: puntero a nullptr
IteradorCalendario Calendario::end() const {
    IteradorCalendario it;
    it.pt = nullptr;
    return it;
}

// Devuelve el evento apuntado por el iterador
Evento Calendario::getEvento(const IteradorCalendario& it) const {
    if (it.pt != nullptr) {
        return it.pt->getEvento();
    } else {
        return Evento();
    }
}

// Añade un evento al calendario
bool Calendario::insertarEvento(const Fecha& f, const string& s) {
    if (comprobarEvento(f)) {
        return false;
    }

    Evento nuevoEvento(f, s);
    NodoCalendario* nuevoNodo = new NodoCalendario();
    nuevoNodo->setEvento(nuevoEvento);
    nuevoNodo->setSiguiente(nullptr);

    if (head == nullptr || nuevoEvento < head->getEvento()) {
        nuevoNodo->setSiguiente(head);
        head = nuevoNodo;
    } else {
        NodoCalendario* actual = head;
        while (actual->getSiguiente() != nullptr && actual->getSiguiente()->getEvento() < nuevoEvento) {
            actual = actual->getSiguiente();
        }
        nuevoNodo->setSiguiente(actual->getSiguiente());
        actual->setSiguiente(nuevoNodo);
    }
    return true;
}

// Elimina un evento del calendario
bool Calendario::eliminarEvento(const Fecha& f) {
    if (head == nullptr) {
        return false;
    }

    if (head->getEvento().getFecha() == f) {
        NodoCalendario* temp = head;
        head = head->getSiguiente();
        delete temp;
        return true;
    }

    NodoCalendario* actual = head;
    while (actual->getSiguiente() != nullptr && actual->getSiguiente()->getEvento().getFecha() != f) {
        actual = actual->getSiguiente();
    }

    if (actual->getSiguiente() == nullptr) {
        return false;
    } else {
        NodoCalendario* temp = actual->getSiguiente();
        actual->setSiguiente(temp->getSiguiente());
        delete temp;
        return true;
    }
}

// Comprueba si hay algún evento asociado a la fecha dada
bool Calendario::comprobarEvento(const Fecha& f) const {
    NodoCalendario* actual = head;
    while (actual != nullptr) {
        if (actual->getEvento().getFecha() == f) {
            return true;
        }
        actual = actual->getSiguiente();
    }
    return false;
}

// Obtiene la descripción asociada al evento
string Calendario::obtenerDescripcion(const Fecha& f) const {
    NodoCalendario* actual = head;
    while (actual != nullptr) {
        if (actual->getEvento().getFecha() == f) {
            return actual->getEvento().getDescripcion();
        }
        actual = actual->getSiguiente();
    }
    return "";
}

// Añade todos los eventos del calendario pasado como parámetro
void Calendario::importarEventos(const Calendario& c) {
    NodoCalendario* actual = c.head;
    while (actual != nullptr) {
        Evento e = actual->getEvento();
        if (!comprobarEvento(e.getFecha())) {
            insertarEvento(e.getFecha(), e.getDescripcion());
        }
        actual = actual->getSiguiente();
    }
}

// Devuelve una cadena con el contenido completo del calendario
string Calendario::aCadena() const {
    string resultado = "";
    NodoCalendario* actual = head;
    while (actual != nullptr) {
        Evento e = actual->getEvento();
        string fechaStr = e.getFecha().aCadena(true, true);
        string descripcion = e.getDescripcion();
        resultado += fechaStr + ":" + descripcion + "\n";
        actual = actual->getSiguiente();
    }
    return resultado;
}

