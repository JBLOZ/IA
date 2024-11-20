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


    // Método para buscar eventos cuya descripción contenga una cadena específica
    std::vector<Evento> buscarPorDescripcion(const std::string& descripcion) const;

    // Método para fusionar otro Calendario con el actual, evitando duplicados
    void fusionarCalendario(const Calendario& otroCalendario);

    // Método para obtener el próximo Evento a partir de una fecha dada
    Evento buscarProximoEvento(const Fecha& f) const;

    // Método para eliminar todos los Eventos que coincidan con una descripción específica
    int eliminarEventosPorDescripcion(const std::string& descripcion);

    // Método para comparar si dos Calendarios son iguales
    bool esIgual(const Calendario& c) const;

    // Método para revertir la lista de eventos de manera iterativa
    void revertirIterativo();

    // Método para revertir la lista de eventos de manera recursiva
    void revertirRecursivo();

    // Método para encontrar el Evento con la descripción más larga
    Evento eventoDescripcionMasLarga() const;

    // Método para guardar los eventos en un archivo de texto
    bool guardarEnArchivo(const std::string& nombreArchivo) const;

    // Método para cargar eventos desde un archivo de texto
    bool cargarDesdeLista(const std::vector<std::pair<Fecha, std::string>>& listaEventos);

    // Método para ordenar los eventos alfabéticamente por descripción
    void ordenarPorDescripcion();
     
    void eliminarEventosDiasPares();

    bool modificarEvento(const Fecha& fechaOriginal, const Fecha& fechaNueva, const std::string& nuevaDescripcion);

    Evento ultimoEvento() const;

    Evento primerEvento() const;

    Evento eventoEnPosicion(int posicion) const;

    Evento buscarEventoPorNombre(const std::string& nombre) const;

    bool eliminarPrimerEvento();

    bool eliminarUltimoEvento();

    int contarEventos() const;

    bool actualizarEvento(const std::string& nombre, const Evento& nuevoEvento);

    void ordenarPorFecha();

    Evento proximoEvento(const Fecha& fechaActual) const;

    Evento eventoAnterior(const Fecha& fechaActual) const;

    bool esVacio() const;

    int contarEventosConDescripcion(const std::string& descripcion) const;

    void eliminarEventosAntesDe(const Fecha& fecha);

    bool actualizarDescripcionEvento(const std::string& descripcionActual, const std::string& nuevaDescripcion);

    void eliminarEventosPorFechaRango(const Fecha& fechaInicio, const Fecha& fechaFin);

    Calendario filtrarEventosPorMes(int mes) const;

    void fusionarCalendarios(const Calendario& otroCalendario);

    NodoCalendario* invertirRecursivo(NodoCalendario* nodo);

    Calendario obtenerEventosEntreFechas(const Fecha& fechaInicio, const Fecha& fechaFin) const;

    Calendario clonarCalendario() const;

    Calendario interseccionarCalendarios(const Calendario& otroCalendario) const;

    void eliminarDuplicados();

    bool actualizarFechaEvento(const std::string& descripcion, const Fecha& nuevaFecha);


};

#endif // CALENDARIO_H