#ifndef EVENTO_H
#define EVENTO_H

#include "Fecha.h"
#include <string>
#include <vector>

using namespace std;

/**
 * @brief Clase que representa un evento en el calendario.
 * 
 * La clase Evento almacena información sobre un evento, incluyendo su fecha, título,
 * descripción y categoría. Asegura que el título nunca esté vacío y que la categoría
 * no sea inferior a -1.
 */
class Evento {
private:
    Fecha fecha;                ///< Fecha del evento
    string titulo;              ///< Título del evento
    string descripcion;         ///< Descripción del evento
    int categoria;              ///< Categoría del evento

public:
    /**
     * @brief Constructor por defecto.
     * 
     * Inicializa la fecha a 1/1/1900, el título a "sin título",
     * la descripción a una cadena vacía y la categoría a -1.
     */
    Evento();

    /**
     * @brief Constructor sobrecargado.
     * 
     * Inicializa la fecha, título, descripción y categoría con los valores proporcionados.
     * Si el título está vacío, se establece a "sin título".
     * Si la categoría es menor que -1, se establece a -1.
     * 
     * @param f Fecha del evento.
     * @param t Título del evento.
     * @param d Descripción del evento.
     * @param c Categoría del evento.
     */
    Evento(const Fecha&, const string&, const string&, int);

    /**
     * @brief Constructor de copia.
     * 
     * Crea una nueva instancia de Evento copiando los atributos de otro Evento.
     * 
     * @param e Evento a copiar.
     */
    Evento(const Evento&);

    /**
     * @brief Operador de asignación.
     * 
     * Asigna los atributos de un Evento a otro.
     * 
     * @param e Evento fuente.
     * @return Referencia al objeto asignado.
     */
    Evento& operator=(const Evento&);

    /**
     * @brief Destructor.
     * 
     * Resetea la fecha a 1/1/1900, el título a "sin título",
     * la descripción a una cadena vacía y la categoría a 0.
     */
    ~Evento();

    /**
     * @brief Operador de igualdad.
     * 
     * Compara dos Eventos y retorna true si tienen la misma fecha, título,
     * descripción y categoría.
     * 
     * @param e Evento a comparar.
     * @return true si los eventos son iguales, false en caso contrario.
     */
    bool operator==(const Evento&) const;

    /**
     * @brief Operador de desigualdad.
     * 
     * Compara dos Eventos y retorna true si alguno de sus atributos difiere.
     * 
     * @param e Evento a comparar.
     * @return true si los eventos son diferentes, false si son iguales.
     */
    bool operator!=(const Evento&) const;

    /**
     * @brief Obtiene la fecha del evento.
     * 
     * Retorna una copia de la fecha del evento.
     * 
     * @return Fecha del evento.
     */
    Fecha getFecha() const;

    /**
     * @brief Obtiene el título del evento.
     * 
     * Retorna una copia del título del evento.
     * 
     * @return Título del evento.
     */
    string getTitulo() const;

    /**
     * @brief Obtiene la descripción del evento.
     * 
     * Retorna una copia de la descripción del evento.
     * 
     * @return Descripción del evento.
     */
    string getDescripcion() const;

    /**
     * @brief Obtiene la categoría del evento.
     * 
     * Retorna el valor entero que representa la categoría del evento.
     * 
     * @return Categoría del evento.
     */
    int getCategoria() const;

    /**
     * @brief Modifica la fecha del evento.
     * 
     * Actualiza la fecha del evento con la fecha proporcionada.
     * 
     * @param f Nueva fecha del evento.
     */
    void setFecha(const Fecha&);

    /**
     * @brief Modifica el título del evento.
     * 
     * Actualiza el título del evento. Si el título proporcionado está vacío,
     * se establece a "sin título".
     * 
     * @param t Nuevo título del evento.
     */
    void setTitulo(const string&);

    /**
     * @brief Modifica la descripción del evento.
     * 
     * Actualiza la descripción del evento con la cadena proporcionada.
     * 
     * @param d Nueva descripción del evento.
     */
    void setDescripcion(const string&);

    /**
     * @brief Modifica la categoría del evento.
     * 
     * Actualiza la categoría del evento. Si la categoría proporcionada es
     * menor que -1, se establece a -1.
     * 
     * @param c Nueva categoría del evento.
     */
    void setCategoria(int);

    /**
     * @brief Convierte el evento a una cadena de texto.
     * 
     * Genera una representación en cadena del evento siguiendo el formato especificado:
     * 
     * "día de la semana día de mes de año:título[categoría]:descripción"
     * 
     * La descripción de la categoría se obtiene del vector proporcionado. Si la categoría
     * es -1, se deja vacío entre los corchetes.
     * 
     * @param categorias Vector que contiene las descripciones de las categorías.
     * @return Cadena que representa el evento.
     */
    string aCadena(const vector<string>&) const;
};

#endif // EVENTO_H