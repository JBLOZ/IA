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
// Elimina todos los eventos que coincidan con una descripción específica
int Calendario::eliminarEventosPorDescripcion(const std::string& descripcion) {
    int contadorEliminados = 0;
    NodoCalendario* actual = head;
    NodoCalendario* previo = nullptr;

    while (actual != nullptr) {
        if (actual->getEvento().getDescripcion() == descripcion) {
            NodoCalendario* temp = actual;
            if (previo == nullptr) {
                head = actual->getSiguiente();
            } else {
                previo->setSiguiente(actual->getSiguiente());
            }
            actual = actual->getSiguiente();
            delete temp;
            contadorEliminados++;
        } else {
            previo = actual;
            actual = actual->getSiguiente();
        }
    }
    return contadorEliminados;
}

// Método que compara si dos Calendarios son iguales (mismos eventos en el mismo orden)
bool Calendario::esIgual(const Calendario& c) const {
    NodoCalendario* actual1 = head;
    NodoCalendario* actual2 = c.head;

    while (actual1 != nullptr && actual2 != nullptr) {
        if (!(actual1->getEvento() == actual2->getEvento())) {
            return false;
        }
        actual1 = actual1->getSiguiente();
        actual2 = actual2->getSiguiente();
    }
    return (actual1 == nullptr && actual2 == nullptr);
}

// Método que encuentra y retorna el evento con la descripción más larga
Evento Calendario::eventoDescripcionMasLarga() const {
    if (head == nullptr) {
        return Evento();
    }

    NodoCalendario* actual = head;
    Evento eventoMax = actual->getEvento();

    while (actual != nullptr) {
        if (actual->getEvento().getDescripcion().length() > eventoMax.getDescripcion().length()) {
            eventoMax = actual->getEvento();
        }
        actual = actual->getSiguiente();
    }
    return eventoMax;
}

// Método que invierte la lista de eventos de manera iterativa
void Calendario::revertirIterativo() {
    NodoCalendario* previo = nullptr;
    NodoCalendario* actual = head;
    NodoCalendario* siguiente = nullptr;

    while (actual != nullptr) {
        siguiente = actual->getSiguiente();
        actual->setSiguiente(previo);
        previo = actual;
        actual = siguiente;
    }
    head = previo;
}

// Método auxiliar recursivo para invertir la lista
NodoCalendario* Calendario::invertirRecursivo(NodoCalendario* nodo) {
    if (nodo == nullptr || nodo->getSiguiente() == nullptr) {
        return nodo;
    }

    NodoCalendario* nuevoHead = invertirRecursivo(nodo->getSiguiente());
    nodo->getSiguiente()->setSiguiente(nodo);
    nodo->setSiguiente(nullptr);
    return nuevoHead;
}

// Método público que inicia la inversión recursiva
void Calendario::revertirRecursivo() {
    head = invertirRecursivo(head);
}

// Método que ordena los eventos alfabéticamente por descripción
void Calendario::ordenarPorDescripcion() {
    if (head == nullptr || head->getSiguiente() == nullptr) {
        return;
    }

    bool cambio;
    do {
        cambio = false;
        NodoCalendario* actual = head;
        NodoCalendario* previo = nullptr;

        while (actual->getSiguiente() != nullptr) {
            NodoCalendario* siguiente = actual->getSiguiente();

            if (actual->getEvento().getDescripcion() > siguiente->getEvento().getDescripcion()) {
                actual->setSiguiente(siguiente->getSiguiente());
                siguiente->setSiguiente(actual);

                if (previo == nullptr) {
                    head = siguiente;
                } else {
                    previo->setSiguiente(siguiente);
                }
                cambio = true;
                previo = siguiente;
            } else {
                previo = actual;
                actual = actual->getSiguiente();
            }
        }
    } while (cambio);
}

// Método que guarda los eventos en un archivo de texto
bool Calendario::guardarEnArchivo(const std::string& nombreArchivo) const {
    std::ofstream archivo(nombreArchivo);
    if (!archivo.is_open()) {
        return false;
    }

    NodoCalendario* actual = head;
    while (actual != nullptr) {
        Evento e = actual->getEvento();
        archivo << e.getDescripcion() << "\n";
        actual = actual->getSiguiente();
    }

    archivo.close();
    return true;
}

bool Calendario::cargarDesdeLista(const std::vector<std::pair<Fecha, std::string>>& listaEventos) {
    for (const auto& evento : listaEventos) {         // Itera sobre cada par de Fecha y Descripción
        const Fecha& fecha = evento.first;            // Obtiene la fecha del evento
        const std::string& descripcion = evento.second; // Obtiene la descripción del evento
        
        insertarEvento(fecha, descripcion);           // Inserta el evento en el calendario
    }
    return true;
}
// Elimina los eventos de los días pares
void Calendario::eliminarEventosDiasPares() {
    NodoCalendario* actual = head;
    NodoCalendario* anterior = nullptr;

    while (actual != nullptr) {
        int dia = actual->getEvento().getFecha().getDia();
        // Si el día es par, se elimina el evento
        if (dia % 2 == 0) {
            if (anterior != nullptr) {
                anterior->setSiguiente(actual->getSiguiente());
                delete actual;
                actual = anterior->getSiguiente();
            } else {
                head = actual->getSiguiente();
                delete actual;
                actual = head;
            }
        } else {
            anterior = actual;
            actual = actual->getSiguiente();
        }
    }
}
 
bool Calendario::modificarEvento(const Fecha& fechaOriginal, const Fecha& fechaNueva, const std::string& nuevaDescripcion) {
    NodoCalendario* actual = head;   // Inicia la búsqueda desde el head
    NodoCalendario* previo = nullptr; // Mantiene referencia al nodo previo

    while (actual != nullptr) {
        Evento eventoActual = actual->getEvento(); // Obtiene una copia del evento actual

        if (eventoActual.getFecha() == fechaOriginal) { // Verifica si es el evento a modificar
            // Verifica si la nueva fecha ya tiene un evento, si es diferente a la original
            if (!(fechaNueva == fechaOriginal) && comprobarEvento(fechaNueva)) {
                // Existe un conflicto, no se puede modificar
                return false;
            }

            // Crea un nuevo Evento con los nuevos detalles
            Evento eventoModificado(fechaNueva, nuevaDescripcion);

            // Actualiza el evento en el nodo usando setEvento()
            actual->setEvento(eventoModificado);

            // Si la fecha ha cambiado, es necesario reinsertar el evento para mantener el orden
            if (!(fechaNueva == fechaOriginal)) {
                // Desenlazar el nodo actual de la lista
                if (previo == nullptr) {
                    // El nodo a eliminar es el head
                    head = actual->getSiguiente();
                } else {
                    previo->setSiguiente(actual->getSiguiente());
                }

                // Guardar una referencia al siguiente nodo antes de eliminar
                NodoCalendario* siguienteNodo = actual->getSiguiente();

                // Eliminar el nodo actual para liberar memoria
                delete actual;

                // Reinsertar el evento modificado en la posición correcta
                bool insertado = insertarEvento(fechaNueva, nuevaDescripcion);

                // Retornar el resultado de la inserción
                return insertado;
            }

            // Si solo se actualizó la descripción sin cambiar la fecha
            return true;
        }

        // Avanza al siguiente nodo
        previo = actual;
        actual = actual->getSiguiente();
    }

    // Evento original no encontrado
    return false;
}

Evento Calendario::ultimoEvento() const {
    if (head == nullptr) { 
        return Evento(); 
    }

    NodoCalendario* actual = head;
    while (actual->getSiguiente() != nullptr) {
        actual = actual->getSiguiente();
    }

    return actual->getEvento();
}

Evento Calendario::primerEvento() const {
    if (head == nullptr) { 
        return Evento(); 
    }

    NodoCalendario* actual = head;
    // No es necesario iterar, ya que head es el primer nodo

    return actual->getEvento();
}

Evento Calendario::eventoEnPosicion(int posicion) const {
    if (head == nullptr || posicion < 0) { 
        return Evento(); 
    }

    NodoCalendario* actual = head;
    int indice = 0;
    while (actual != nullptr && indice < posicion) {
        actual = actual->getSiguiente();
        indice++;
    }

    if (actual == nullptr) {
        return Evento(); // Posición fuera de rango
    }

    return actual->getEvento();
}
Evento Calendario::buscarEventoPorNombre(const std::string& nombre) const {
    NodoCalendario* actual = head;
    while (actual != nullptr) {
        if (actual->getEvento().getDescripcion() == nombre) {
            return actual->getEvento();
        }
        actual = actual->getSiguiente();
    }
    return Evento(); // Evento no encontrado
}

bool Calendario::eliminarPrimerEvento() {
    if (head == nullptr) {
        return false; // Lista vacía
    }

    NodoCalendario* temp = head;
    head = head->getSiguiente();
    delete temp;
    return true;
}

bool Calendario::eliminarUltimoEvento() {
    if (head == nullptr) {
        return false; // Lista vacía
    }

    if (head->getSiguiente() == nullptr) {
        delete head;
        head = nullptr;
        return true;
    }

    NodoCalendario* actual = head;
    NodoCalendario* anterior = nullptr;
    while (actual->getSiguiente() != nullptr) {
        anterior = actual;
        actual = actual->getSiguiente();
    }

    anterior->setSiguiente(nullptr);
    delete actual;
    return true;
}

int Calendario::contarEventos() const {
    int contador = 0;
    NodoCalendario* actual = head;
    while (actual != nullptr) {
        contador++;
        actual = actual->getSiguiente();
    }
    return contador;
}

bool Calendario::actualizarEvento(const std::string& nombre, const Evento& nuevoEvento) {
    NodoCalendario* actual = head;
    while (actual != nullptr) {
        if (actual->getEvento().getDescripcion() == nombre) {
            actual->setEvento(nuevoEvento);
            return true;
        }
        actual = actual->getSiguiente();
    }
    return false; // Evento no encontrado
}

void Calendario::ordenarPorFecha() {
    if (head == nullptr || head->getSiguiente() == nullptr) {
        return; // Lista vacía o con un solo elemento
    }

    bool intercambiado;
    do {
        intercambiado = false;
        NodoCalendario* actual = head;
        NodoCalendario* previo = nullptr;

        while (actual->getSiguiente() != nullptr) {
            if (actual->getEvento().getFecha() > actual->getSiguiente()->getEvento().getFecha()) {
                // Intercambiar nodos
                NodoCalendario* siguiente = actual->getSiguiente();
                actual->setSiguiente(siguiente->getSiguiente());
                siguiente->setSiguiente(actual);

                if (previo == nullptr) {
                    head = siguiente;
                } else {
                    previo->setSiguiente(siguiente);
                }

                intercambiado = true;
                previo = siguiente;
            } else {
                previo = actual;
                actual = actual->getSiguiente();
            }
        }
    } while (intercambiado);
}

Evento Calendario::proximoEvento(const Fecha& fechaActual) const {
    NodoCalendario* actual = head;
    Evento proximo;
    bool encontrado = false;

    while (actual != nullptr) {
        if (actual->getEvento().getFecha() > fechaActual) {
            if (!encontrado || actual->getEvento().getFecha() < proximo.getFecha()) {
                proximo = actual->getEvento();
                encontrado = true;
            }
        }
        actual = actual->getSiguiente();
    }

    if (encontrado) {
        return proximo;
    } else {
        return Evento(); // No hay eventos futuros
    }
}

// Método para obtener el evento anterior antes de una fecha específica
Evento Calendario::eventoAnterior(const Fecha& fechaActual) const {
    NodoCalendario* actual = head;
    Evento anterior;
    bool encontrado = false;

    while (actual != nullptr) {
        if (actual->getEvento().getFecha() < fechaActual) {
            if (!encontrado || actual->getEvento().getFecha() > anterior.getFecha()) {
                anterior = actual->getEvento();
                encontrado = true;
            }
        }
        actual = actual->getSiguiente();
    }

    if (encontrado) {
        return anterior;
    } else {
        return Evento(); // No hay eventos anteriores
    }
}
bool Calendario::esVacio() const {
    return head == nullptr;
}

int Calendario::contarEventosConDescripcion(const std::string& descripcion) const {
    int contador = 0;
    NodoCalendario* actual = head;
    while (actual != nullptr) {
        if (actual->getEvento().getDescripcion() == descripcion) {
            contador++;
        }
        actual = actual->getSiguiente();
    }
    return contador;
}

void Calendario::eliminarEventosAntesDe(const Fecha& fecha) {
    while (head != nullptr && head->getEvento().getFecha() < fecha) {
        NodoCalendario* temp = head;
        head = head->getSiguiente();
        delete temp;
    }

    NodoCalendario* actual = head;
    NodoCalendario* previo = nullptr;

    while (actual != nullptr) {
        if (actual->getEvento().getFecha() < fecha) {
            NodoCalendario* temp = actual;
            if (previo != nullptr) {
                previo->setSiguiente(actual->getSiguiente());
            }
            actual = actual->getSiguiente();
            delete temp;
        } else {
            previo = actual;
            actual = actual->getSiguiente();
        }
    }
}

bool Calendario::actualizarDescripcionEvento(const std::string& descripcionActual, const std::string& nuevaDescripcion) {
    NodoCalendario* actual = head;
    while (actual != nullptr) {
        if (actual->getEvento().getDescripcion() == descripcionActual) {
            Evento eventoModificado = actual->getEvento();
            eventoModificado.setDescripcion(nuevaDescripcion);
            actual->setEvento(eventoModificado);
            return true;
        }
        actual = actual->getSiguiente();
    }
    return false; // Evento no encontrado
}

void Calendario::eliminarEventosPorFechaRango(const Fecha& fechaInicio, const Fecha& fechaFin) {
    while (head != nullptr && head->getEvento().getFecha() > fechaInicio && head->getEvento().getFecha() < fechaFin) {
        NodoCalendario* temp = head;
        head = head->getSiguiente();
        delete temp;
    }

    NodoCalendario* actual = head;
    NodoCalendario* previo = nullptr;

    while (actual != nullptr) {
        if (actual->getEvento().getFecha() > fechaInicio && actual->getEvento().getFecha() < fechaFin) {
            NodoCalendario* temp = actual;
            if (previo != nullptr) {
                previo->setSiguiente(actual->getSiguiente());
            }
            actual = actual->getSiguiente();
            delete temp;
        } else {
            previo = actual;
            actual = actual->getSiguiente();
        }
    }
}

Calendario Calendario::filtrarEventosPorMes(int mes) const {
    Calendario filtrado;
    NodoCalendario* actual = head;
    while (actual != nullptr) {
        if (actual->getEvento().getFecha().getMes() == mes) {
            filtrado.insertarEvento(actual->getEvento().getFecha(), actual->getEvento().getDescripcion());
        }
        actual = actual->getSiguiente();
    }
    return filtrado;
}

void Calendario::fusionarCalendarios(const Calendario& otroCalendario) {
    NodoCalendario* actual = otroCalendario.head;
    while (actual != nullptr) {
        this->insertarEvento(actual->getEvento().getFecha(), actual->getEvento().getDescripcion());
        actual = actual->getSiguiente();
    }
}

Calendario Calendario::obtenerEventosEntreFechas(const Fecha& fechaInicio, const Fecha& fechaFin) const {
    Calendario eventosEntre;
    NodoCalendario* actual = head;
    while (actual != nullptr) {
        Fecha fechaEvento = actual->getEvento().getFecha();
        if (fechaEvento > fechaInicio && fechaEvento < fechaFin) {
            eventosEntre.insertarEvento(fechaEvento, actual->getEvento().getDescripcion());
        }
        actual = actual->getSiguiente();
    }
    return eventosEntre;
}

Calendario Calendario::clonarCalendario() const {
    Calendario clon;
    NodoCalendario* actual = head;
    while (actual != nullptr) {
        clon.insertarEvento(actual->getEvento().getFecha(), actual->getEvento().getDescripcion());
        actual = actual->getSiguiente();
    }
    return clon;
}

Calendario Calendario::interseccionarCalendarios(const Calendario& otroCalendario) const {
    Calendario interseccion;
    NodoCalendario* actual = head;
    while (actual != nullptr) {
        if (otroCalendario.comprobarEvento(actual->getEvento().getFecha()) &&
            otroCalendario.obtenerDescripcion(actual->getEvento().getFecha()) == actual->getEvento().getDescripcion()) {
            interseccion.insertarEvento(actual->getEvento().getFecha(), actual->getEvento().getDescripcion());
        }
        actual = actual->getSiguiente();
    }
    return interseccion;
}

void Calendario::eliminarDuplicados() {
    NodoCalendario* actual = head;
    while (actual != nullptr) {
        NodoCalendario* buscador = actual;
        while (buscador->getSiguiente() != nullptr) {
            if (buscador->getSiguiente()->getEvento().getFecha() == actual->getEvento().getFecha() &&
                buscador->getSiguiente()->getEvento().getDescripcion() == actual->getEvento().getDescripcion()) {
                NodoCalendario* temp = buscador->getSiguiente();
                buscador->setSiguiente(temp->getSiguiente());
                delete temp;
            } else {
                buscador = buscador->getSiguiente();
            }
        }
        actual = actual->getSiguiente();
    }
}

bool Calendario::actualizarFechaEvento(const std::string& descripcion, const Fecha& nuevaFecha) {
    NodoCalendario* actual = head;
    NodoCalendario* previo = nullptr;

    while (actual != nullptr) {
        if (actual->getEvento().getDescripcion() == descripcion) {
            // Verificar si la nueva fecha ya tiene un evento
            if (comprobarEvento(nuevaFecha)) {
                return false; // Conflicto de fechas
            }

            // Actualizar el evento
            Evento eventoModificado = actual->getEvento();
            eventoModificado.setFecha(nuevaFecha);
            actual->setEvento(eventoModificado);

            // Reubicar el nodo para mantener el orden
            if (previo != nullptr) {
                previo->setSiguiente(actual->getSiguiente());
            } else {
                head = actual->getSiguiente();
            }

            // Reinserción del evento actualizado
            NodoCalendario* siguiente = actual->getSiguiente();
            actual->setSiguiente(nullptr);
            insertarEvento(nuevaFecha, eventoModificado.getDescripcion());

            return true;
        }
        previo = actual;
        actual = actual->getSiguiente();
    }

    return false; // Evento no encontrado
}

