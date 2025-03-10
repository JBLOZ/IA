#ifndef CALENDARIO_H
#define CALENDARIO_H

#include <string>
#include <vector>
#include <fstream>

// Asumiendo que las clases Evento y Fecha están definidas en otros archivos de cabecera
#include "Evento.h"
#include "Fecha.h"

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
  // Método para contar el número total de eventos en el calendario
    void filtraEventosMes(int);
    Evento eventoPosterior(Fecha);


};

#endif // CALENDARIO_H