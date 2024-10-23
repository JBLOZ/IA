#include "Calendario.h"

/*** NodoCalendario ***/

// Constructor por defecto
NodoCalendario::NodoCalendario() {
    siguiente = nullptr;
    evento = Evento(); // Evento por defecto
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


// #include "Calendario.h"

// /*** NodoCalendario ***/

// //Constructor por defecto
// NodoCalendario::NodoCalendario(){
// }
// //Constructor sobrecargado
// NodoCalendario::NodoCalendario( NodoCalendario* s, const Evento& e){
// }

// //Constructor de copia
// NodoCalendario::NodoCalendario(const NodoCalendario& nc){
// }

// //Operador de asignación
// NodoCalendario& NodoCalendario::operator=(const NodoCalendario &nc){
// }

// //Destructor
// NodoCalendario::~NodoCalendario(){
// }

// //Devuelve el puntero al siguiente nodo de la lista
// NodoCalendario* NodoCalendario::getSiguiente() const{

// }

// //Devuelve el evento almacenado en el nodo
// Evento NodoCalendario::getEvento() const{
// }

// //Modifica el puntero al siguiente nodo de la lista
// void NodoCalendario::setSiguiente(NodoCalendario* s){
// }

// //Modifica el evento
// void NodoCalendario::setEvento(const Evento& e){
// }


// /*** IteradorCalendario ***/
// //Constructor por defecto: puntero a nullptr
// IteradorCalendario::IteradorCalendario(){
// }

// //Constructor de copia
// IteradorCalendario::IteradorCalendario(const IteradorCalendario& ic){
// }

// //Destructor: puntero a nullptr
// IteradorCalendario::~IteradorCalendario(){
// }

// //Operador de asignación
// IteradorCalendario& IteradorCalendario::operator=(const IteradorCalendario& ic){
// }

// //Incrementa el iterador en un paso
// void IteradorCalendario::step(){
// }

// //Operador de comparación
// bool IteradorCalendario::operator==(const IteradorCalendario& ic) const{
// }

// //Operador de comparación
// bool IteradorCalendario::operator!=(const IteradorCalendario& ic) const{
// }



// /*** Calendario ***/

// //Constructor por defecto: calendario sin ningún evento
// Calendario::Calendario(){
// }

// //Constructor de copia
// Calendario::Calendario(const Calendario& c){
// }

// //Operador de asignación
// Calendario& Calendario::operator=(const Calendario &c){
// }

// //Destructor
// Calendario::~Calendario(){
// }

// //Devuelve un iterador al comienzo del calendario
// IteradorCalendario Calendario::begin() const{
// }

// //Devuelve un iterador al final del calendario: puntero a nullptr
// IteradorCalendario Calendario::end() const{
// }

// //Devuelve el evento apuntado por el iterador
// Evento Calendario::getEvento(const IteradorCalendario & it) const{
// }

// //Añade un evento al calendario. Si ya existía un evento en esa fecha, 
// //devuelve false y no hace nada. En caso contrario, devuelve true.
// bool Calendario::insertarEvento(const Fecha&f,  const string& s){
// }

// //Elimina un evento del calendario. Si no había ningún evento asociado a esa fecha, 
// //devuelve false y no hace nada. En caso contrario, devuelve true.
// bool Calendario::eliminarEvento(const Fecha& f){
// }


// //Comprueba si hay algún evento asociado a la fecha dada
// bool Calendario::comprobarEvento(const Fecha &f) const{
// }


// //Obtiene la descripción asociada al evento. Si no hay ningún evento asociado a la fecha, 
// //devuelve la cadena vacía
// string Calendario::obtenerDescripcion(const Fecha&f) const{
// }

// //Añade todos los eventos del calendario que se pasa como parámetro al calendario actual, 
// //excepto los que están en una fecha que ya existe en el calendario
// void Calendario::importarEventos(const Calendario& c){
// }

// //Devuelve una cadena con el contenido completo del calendario
// string Calendario::aCadena() const{
// }
