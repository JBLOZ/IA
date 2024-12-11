#ifndef CALENDARIO_H
#define CALENDARIO_H

#include "Evento.h"
#include <map>
#include <stack>
#include <vector>
#include <string>

class Calendario {
private:
    // Mapa para almacenar eventos ordenados por fecha
    std::map<Fecha, Evento> eventos;

    // Pilas para el historial de inserciones y borrados
    std::stack<Fecha> historialInserciones;
    std::stack<Evento> historialBorrados;

public:
    // Constructor por defecto
    Calendario();

    // Constructor de copia
    Calendario(const Calendario&);

    // Operador de asignación
    Calendario& operator=(const Calendario&);

    // Destructor
    ~Calendario();

    // Métodos según las especificaciones
    bool insertarEvento(const Evento&);
    bool eliminarEvento(const Fecha&);
    bool comprobarEvento(const Fecha&) const;
    Evento obtenerEvento(const Fecha&) const;
    std::string aCadena(const std::vector<std::string>&) const;
    void deshacerInsercion();
    void deshacerBorrado();
    std::string aCadenaPorTitulo(const std::string&, const std::vector<std::string>&) const;
    int categoriaMasFrecuente() const;
    int diaMasFrecuente() const;
    int mesMasFrecuente() const;
    int anyoMasFrecuente() const;
};

#endif // CALENDARIO_H