#include "Calendario.h" // Incluye la definición de las clases y funciones relacionadas con el calendario
#include <iostream>
#include <fstream>

/*** NodoCalendario ***/

// Constructor por defecto
NodoCalendario::NodoCalendario() {
    siguiente = nullptr;       // Inicializa el puntero al siguiente nodo como nullptr (no apunta a nada)
    evento = Evento();         // Inicializa el evento con el constructor por defecto de la clase Evento
}

// Constructor sobrecargado
NodoCalendario::NodoCalendario(NodoCalendario* s, const Evento& e) {
    siguiente = s;             // Asigna el puntero al siguiente nodo con el valor pasado como argumento
    evento = e;                // Asigna el evento con el valor pasado como argumento
}

// Constructor de copia
NodoCalendario::NodoCalendario(const NodoCalendario& nc) {
    siguiente = nc.siguiente;  // Copia el puntero al siguiente nodo del nodo fuente
    evento = nc.evento;        // Copia el evento del nodo fuente
}

// Operador de asignación
NodoCalendario& NodoCalendario::operator=(const NodoCalendario& nc) {
    if (this != &nc) {                     // Verifica que no se esté asignando el objeto a sí mismo
        siguiente = nc.siguiente;           // Copia el puntero al siguiente nodo del nodo fuente
        evento = nc.evento;                 // Copia el evento del nodo fuente
    }
    return *this;                           // Devuelve una referencia al objeto actual para permitir encadenamiento
}

// Destructor
NodoCalendario::~NodoCalendario() {
    // No se libera memoria aquí; se maneja desde Calendario
    siguiente = nullptr;                    // Establece el puntero al siguiente nodo a nullptr para evitar referencias colgantes
}

// Devuelve el puntero al siguiente nodo de la lista
NodoCalendario* NodoCalendario::getSiguiente() const {
    return siguiente;                       // Retorna el puntero al siguiente nodo
}

// Devuelve el evento almacenado en el nodo
Evento NodoCalendario::getEvento() const {
    return evento;                          // Retorna el evento almacenado en el nodo
}

// Modifica el puntero al siguiente nodo de la lista
void NodoCalendario::setSiguiente(NodoCalendario* s) {
    siguiente = s;                          // Asigna el puntero al siguiente nodo con el valor pasado como argumento
}

// Modifica el evento
void NodoCalendario::setEvento(const Evento& e) {
    evento = e;                             // Asigna el evento con el valor pasado como argumento
}

/*** IteradorCalendario ***/

// Constructor por defecto: puntero a nullptr
IteradorCalendario::IteradorCalendario() {
    pt = nullptr;                           // Inicializa el puntero del iterador a nullptr (no apunta a ningún nodo)
}

// Constructor de copia
IteradorCalendario::IteradorCalendario(const IteradorCalendario& ic) {
    pt = ic.pt;                             // Copia el puntero del iterador fuente
}

// Destructor: puntero a nullptr
IteradorCalendario::~IteradorCalendario() {
    pt = nullptr;                           // Establece el puntero del iterador a nullptr
}

// Operador de asignación
IteradorCalendario& IteradorCalendario::operator=(const IteradorCalendario& ic) {
    if (this != &ic) {                      // Verifica que no se esté asignando el iterador a sí mismo
        pt = ic.pt;                          // Copia el puntero del iterador fuente
    }
    return *this;                            // Devuelve una referencia al iterador actual para permitir encadenamiento
}

// Incrementa el iterador en un paso
void IteradorCalendario::step() {
    if (pt != nullptr) {                     // Verifica que el puntero actual no sea nullptr
        pt = pt->getSiguiente();             // Avanza el puntero al siguiente nodo de la lista
    }
}

// Operador de comparación: igual
bool IteradorCalendario::operator==(const IteradorCalendario& ic) const {
    return pt == ic.pt;                      // Retorna true si ambos iteradores apuntan al mismo nodo
}

// Operador de comparación: diferente
bool IteradorCalendario::operator!=(const IteradorCalendario& ic) const {
    return pt != ic.pt;                      // Retorna true si los iteradores apuntan a nodos diferentes
}

/*** Calendario ***/

// Constructor por defecto: calendario sin ningún evento
Calendario::Calendario() {
    head = nullptr;                          // Inicializa el puntero al inicio de la lista (head) como nullptr
}

// Constructor de copia
Calendario::Calendario(const Calendario& c) {
    head = nullptr;                          // Inicializa el head como nullptr antes de comenzar a copiar
    NodoCalendario* actual = c.head;         // Puntero para recorrer la lista del calendario fuente
    NodoCalendario* previo = nullptr;        // Puntero para mantener el nodo previo durante la copia

    // Recorre cada nodo del calendario fuente
    while (actual != nullptr) {
        NodoCalendario* nuevoNodo = new NodoCalendario(); // Crea un nuevo nodo
        nuevoNodo->setEvento(actual->getEvento());        // Copia el evento del nodo fuente al nuevo nodo
        nuevoNodo->setSiguiente(nullptr);                  // Inicializa el siguiente nodo como nullptr

        if (head == nullptr) {                             // Si la lista está vacía
            head = nuevoNodo;                              // Establece el nuevo nodo como el head de la lista
        } else {
            previo->setSiguiente(nuevoNodo);               // Enlaza el nuevo nodo al final de la lista copiada
        }

        previo = nuevoNodo;                                 // Actualiza el puntero previo al nuevo nodo
        actual = actual->getSiguiente();                    // Avanza al siguiente nodo en la lista fuente
    }
}

// Operador de asignación
Calendario& Calendario::operator=(const Calendario& c) {
    if (this != &c) {                                      // Verifica que no se esté asignando el calendario a sí mismo
        // Liberar la lista actual
        NodoCalendario* actual = head;                     // Puntero para recorrer la lista actual
        while (actual != nullptr) {                        // Mientras no se llegue al final de la lista
            NodoCalendario* temp = actual;                  // Guarda el nodo actual en un puntero temporal
            actual = actual->getSiguiente();                // Avanza al siguiente nodo
            delete temp;                                    // Elimina el nodo actual para liberar memoria
        }
        head = nullptr;                                     // Establece head como nullptr después de eliminar todos los nodos

        // Copiar desde c
        actual = c.head;                                    // Reinicia el puntero para copiar desde el calendario fuente
        NodoCalendario* previo = nullptr;                   // Puntero previo para mantener la referencia del último nodo copiado

        // Recorre cada nodo del calendario fuente
        while (actual != nullptr) {
            NodoCalendario* nuevoNodo = new NodoCalendario(); // Crea un nuevo nodo
            nuevoNodo->setEvento(actual->getEvento());        // Copia el evento del nodo fuente al nuevo nodo
            nuevoNodo->setSiguiente(nullptr);                  // Inicializa el siguiente nodo como nullptr

            if (head == nullptr) {                             // Si la lista está vacía
                head = nuevoNodo;                              // Establece el nuevo nodo como el head de la lista
            } else {
                previo->setSiguiente(nuevoNodo);               // Enlaza el nuevo nodo al final de la lista copiada
            }

            previo = nuevoNodo;                                 // Actualiza el puntero previo al nuevo nodo
            actual = actual->getSiguiente();                    // Avanza al siguiente nodo en la lista fuente
        }
    }
    return *this;                                            // Devuelve una referencia al calendario actual para permitir encadenamiento
}

// Destructor
Calendario::~Calendario() {
    NodoCalendario* actual = head;                         // Puntero para recorrer la lista desde el head
    while (actual != nullptr) {                            // Mientras no se llegue al final de la lista
        NodoCalendario* temp = actual;                      // Guarda el nodo actual en un puntero temporal
        actual = actual->getSiguiente();                    // Avanza al siguiente nodo
        delete temp;                                        // Elimina el nodo actual para liberar memoria
    }
    head = nullptr;                                         // Establece head como nullptr después de eliminar todos los nodos
}

// Devuelve un iterador al comienzo del calendario
IteradorCalendario Calendario::begin() const {
    IteradorCalendario it;                                  // Crea una instancia de IteradorCalendario
    it.pt = head;                                           // Establece el puntero del iterador al head de la lista
    return it;                                               // Devuelve el iterador
}

// Devuelve un iterador al final del calendario: puntero a nullptr
IteradorCalendario Calendario::end() const {
    IteradorCalendario it;                                  // Crea una instancia de IteradorCalendario
    it.pt = nullptr;                                        // Establece el puntero del iterador a nullptr para indicar el final
    return it;                                               // Devuelve el iterador
}

// Devuelve el evento apuntado por el iterador
Evento Calendario::getEvento(const IteradorCalendario& it) const {
    if (it.pt != nullptr) {                                 // Verifica que el iterador no esté al final
        return it.pt->getEvento();                          // Retorna el evento del nodo apuntado por el iterador
    } else {
        return Evento();                                    // Retorna un evento por defecto si el iterador está al final
    }
}

// Añade un evento al calendario
bool Calendario::insertarEvento(const Fecha& f, const string& s) {
    if (comprobarEvento(f)) {                               // Verifica si ya existe un evento en la fecha dada
        return false;                                       // Retorna false si ya existe un evento en esa fecha
    }

    Evento nuevoEvento(f, s);                                // Crea un nuevo evento con la fecha y descripción proporcionadas
    NodoCalendario* nuevoNodo = new NodoCalendario();       // Crea un nuevo nodo
    nuevoNodo->setEvento(nuevoEvento);                      // Asigna el nuevo evento al nodo
    nuevoNodo->setSiguiente(nullptr);                        // Inicializa el siguiente nodo como nullptr

    // Inserta el nuevo nodo en la posición correcta para mantener la lista ordenada
    if (head == nullptr || nuevoEvento < head->getEvento()) {
        nuevoNodo->setSiguiente(head);                       // Enlaza el nuevo nodo al inicio de la lista
        head = nuevoNodo;                                    // Actualiza el head al nuevo nodo
    } else {
        NodoCalendario* actual = head;                       // Puntero para recorrer la lista
        while (actual->getSiguiente() != nullptr && actual->getSiguiente()->getEvento() < nuevoEvento) {
            actual = actual->getSiguiente();                 // Avanza al siguiente nodo mientras no se alcance el final y el siguiente evento sea menor
        }
        nuevoNodo->setSiguiente(actual->getSiguiente());     // Enlaza el nuevo nodo al siguiente nodo
        actual->setSiguiente(nuevoNodo);                     // Enlaza el nodo actual al nuevo nodo
    }
    return true;                                            // Retorna true indicando que el evento fue insertado correctamente
}

// Elimina un evento del calendario
bool Calendario::eliminarEvento(const Fecha& f) {
    if (head == nullptr) {                                   // Verifica si la lista está vacía
        return false;                                       // Retorna false si no hay nada que eliminar
    }

    if (head->getEvento().getFecha() == f) {                // Verifica si el evento a eliminar está en el head
        NodoCalendario* temp = head;                         // Guarda el nodo head en un puntero temporal
        head = head->getSiguiente();                         // Actualiza el head al siguiente nodo
        delete temp;                                         // Elimina el nodo antiguo del head para liberar memoria
        return true;                                         // Retorna true indicando que el evento fue eliminado
    }

    NodoCalendario* actual = head;                           // Puntero para recorrer la lista
    while (actual->getSiguiente() != nullptr && actual->getSiguiente()->getEvento().getFecha() != f) {
        actual = actual->getSiguiente();                     // Avanza al siguiente nodo mientras no se alcance el final y no se encuentre la fecha
    }

    if (actual->getSiguiente() == nullptr) {                 // Verifica si se llegó al final sin encontrar el evento
        return false;                                       // Retorna false si no se encontró el evento
    } else {
        NodoCalendario* temp = actual->getSiguiente();       // Guarda el nodo a eliminar en un puntero temporal
        actual->setSiguiente(temp->getSiguiente());         // Enlaza el nodo actual al siguiente del nodo a eliminar
        delete temp;                                         // Elimina el nodo a eliminar para liberar memoria
        return true;                                         // Retorna true indicando que el evento fue eliminado
    }
}

// Comprueba si hay algún evento asociado a la fecha dada
bool Calendario::comprobarEvento(const Fecha& f) const {
    NodoCalendario* actual = head;                           // Puntero para recorrer la lista desde el head
    while (actual != nullptr) {                              // Mientras no se llegue al final de la lista
        if (actual->getEvento().getFecha() == f) {          // Verifica si la fecha del evento actual coincide con la fecha dada
            return true;                                     // Retorna true si se encuentra un evento con la fecha dada
        }
        actual = actual->getSiguiente();                     // Avanza al siguiente nodo
    }
    return false;                                            // Retorna false si no se encuentra ningún evento con la fecha dada
}

// Obtiene la descripción asociada al evento
string Calendario::obtenerDescripcion(const Fecha& f) const {
    NodoCalendario* actual = head;                           // Puntero para recorrer la lista desde el head
    while (actual != nullptr) {                              // Mientras no se llegue al final de la lista
        if (actual->getEvento().getFecha() == f) {          // Verifica si la fecha del evento actual coincide con la fecha dada
            return actual->getEvento().getDescripcion();    // Retorna la descripción del evento si se encuentra la fecha
        }
        actual = actual->getSiguiente();                     // Avanza al siguiente nodo
    }
    return "";                                               // Retorna una cadena vacía si no se encuentra ningún evento con la fecha dada
}

// Añade todos los eventos del calendario pasado como parámetro
void Calendario::importarEventos(const Calendario& c) {
    NodoCalendario* actual = c.head;                         // Puntero para recorrer la lista del calendario pasado como parámetro
    while (actual != nullptr) {                              // Mientras no se llegue al final de la lista
        Evento e = actual->getEvento();                      // Obtiene el evento actual
        if (!comprobarEvento(e.getFecha())) {                // Verifica si el evento no está ya en el calendario actual
            insertarEvento(e.getFecha(), e.getDescripcion()); // Inserta el evento en el calendario actual
        }
        actual = actual->getSiguiente();                     // Avanza al siguiente nodo
    }
}

// Devuelve una cadena con el contenido completo del calendario
string Calendario::aCadena() const {
    string resultado = "";                                    // Inicializa una cadena vacía para almacenar el resultado
    NodoCalendario* actual = head;                           // Puntero para recorrer la lista desde el head
    while (actual != nullptr) {                              // Mientras no se llegue al final de la lista
        Evento e = actual->getEvento();                      // Obtiene el evento actual
        string fechaStr = e.getFecha().aCadena(true, true);   // Convierte la fecha del evento a una cadena de texto
        string descripcion = e.getDescripcion();               // Obtiene la descripción del evento
        resultado += fechaStr + ":" + descripcion + "\n";      // Añade la información del evento a la cadena resultado
        actual = actual->getSiguiente();                       // Avanza al siguiente nodo
    }
    return resultado;                                         // Retorna la cadena con todos los eventos
}

void Calendario::filtraEventosMes(int mes)
{
   //Comprobar que "mes" está entre 1 y 12. Si no lo está, salir

   Calendario aux;
   NodoCalendario* actual = head;

   while (actual != nullptr) {
        if (actual->getEvento().getFecha().getMes() == mes) {
            aux.insertarEvento(actual->getEvento().getFecha(), actual->getEvento().getDescripcion());
        }
        actual = actual->getSiguiente();
    }

   //Iterar sobre los eventos del calendario actual
   //Invocar aux.insertarEvento(...) con cada evento que pertenezca al mes pasado como parámetro

   
   (*this)=aux;
   
}

Evento Calendario::eventoPosterior(Fecha f)
{
    NodoCalendario* actual = head;
    while (actual != nullptr) {
        if (f > actual->getEvento().getFecha())
        {
            return actual->getEvento();
        }
        actual = actual->getSiguiente();
    }
    
    Evento evento_si_no_hay_mas = Evento(Fecha(1,1,1900),"No hay eventos posteriores");
    return evento_si_no_hay_mas; 

}