#include "Calendario.h"
#include <unordered_map>

// Constructor por defecto
Calendario::Calendario() {
    // El mapa y las pilas se inicializan automáticamente
}

// Constructor de copia
Calendario::Calendario(const Calendario& c) : eventos(c.eventos), historialInserciones(c.historialInserciones), historialBorrados(c.historialBorrados) {
    // Copia profunda de los miembros
}

// Operador de asignación
Calendario& Calendario::operator=(const Calendario& c) {
    if (this != &c) {
        eventos = c.eventos;
        historialInserciones = c.historialInserciones;
        historialBorrados = c.historialBorrados;
    }
    return *this;
}

// Destructor
Calendario::~Calendario() {
    // Los contenedores de la STL manejan su propia destrucción
}

// Método para insertar un evento
bool Calendario::insertarEvento(const Evento& e) {
    const Fecha& fecha = e.getFecha();
    auto result = eventos.insert({fecha, e});
    if (!result.second) {
        // Ya existe un evento en esa fecha
        return false;
    }
    // Registrar la inserción para deshacer
    historialInserciones.push(fecha);
    return true;
}

// Método para eliminar un evento
bool Calendario::eliminarEvento(const Fecha& fecha) {
    auto it = eventos.find(fecha);
    if (it == eventos.end()) {
        // No hay evento en esa fecha
        return false;
    }
    // Registrar el borrado para deshacer
    historialBorrados.push(it->second);
    eventos.erase(it);
    return true;
}

// Método para comprobar si hay un evento en una fecha
bool Calendario::comprobarEvento(const Fecha& fecha) const {
    return eventos.find(fecha) != eventos.end();
}

// Método para obtener un evento en una fecha
Evento Calendario::obtenerEvento(const Fecha& fecha) const {
    auto it = eventos.find(fecha);
    if (it != eventos.end()) {
        return it->second;
    }
    // Retornar un evento por defecto si no se encuentra
    return Evento();
}

// Método para convertir el calendario a cadena
std::string Calendario::aCadena(const std::vector<std::string>& categorias) const {
    std::string resultado;
    for (auto it = eventos.begin(); it != eventos.end(); ++it) {
        if (!resultado.empty()) {
            resultado += "\n";
        }
        resultado += it->second.aCadena(categorias);
    }
    return resultado;
}

// Método para deshacer la última inserción
void Calendario::deshacerInsercion() {
    if (historialInserciones.empty()) {
        // No hay inserciones para deshacer
        return;
    }
    Fecha fecha = historialInserciones.top();
    historialInserciones.pop();
    eventos.erase(fecha);
}

// Método para deshacer el último borrado
void Calendario::deshacerBorrado() {
    if (historialBorrados.empty()) {
        // No hay borrados para deshacer
        return;
    }
    Evento evento = historialBorrados.top();
    historialBorrados.pop();
    eventos[evento.getFecha()] = evento;
}

// Método para convertir a cadena filtrando por título
std::string Calendario::aCadenaPorTitulo(const std::string& tituloBuscado, const std::vector<std::string>& categorias) const {
    std::string resultado;
    for (const auto& par : eventos) {
        const Evento& evento = par.second;
        if (evento.getTitulo() == tituloBuscado) {
            if (!resultado.empty()) {
                resultado += "\n";
            }
            resultado += evento.aCadena(categorias);
        }
    }
    return resultado;
}

// Método para obtener la categoría más frecuente
int Calendario::categoriaMasFrecuente() const {
    if (eventos.empty()) {
        return -2;
    }
    std::unordered_map<int, int> conteoCategorias;
    for (const auto& par : eventos) {
        int categoria = par.second.getCategoria();
        conteoCategorias[categoria]++;
    }
    // Encontrar la categoría con mayor frecuencia
    int maxCategoria = -1;
    int maxConteo = 0;
    for (const auto& par : conteoCategorias) {
        int categoria = par.first;
        int conteo = par.second;
        if (conteo > maxConteo || (conteo == maxConteo && categoria > maxCategoria)) {
            maxCategoria = categoria;
            maxConteo = conteo;
        }
    }
    return maxCategoria;
}

// Método para obtener el día del mes más frecuente
int Calendario::diaMasFrecuente() const {
    if (eventos.empty()) {
        return -2;
    }
    std::unordered_map<int, int> conteoDias;
    for (const auto& par : eventos) {
        int dia = par.first.getDia();
        conteoDias[dia]++;
    }
    // Encontrar el día con mayor frecuencia
    int maxDia = -1;
    int maxConteo = 0;
    for (const auto& par : conteoDias) {
        int dia = par.first;
        int conteo = par.second;
        if (conteo > maxConteo || (conteo == maxConteo && dia > maxDia)) {
            maxDia = dia;
            maxConteo = conteo;
        }
    }
    return maxDia;
}

// Método para obtener el mes más frecuente
int Calendario::mesMasFrecuente() const {
    if (eventos.empty()) {
        return -2;
    }
    std::unordered_map<int, int> conteoMeses;
    for (const auto& par : eventos) {
        int mes = par.first.getMes();
        conteoMeses[mes]++;
    }
    // Encontrar el mes con mayor frecuencia
    int maxMes = -1;
    int maxConteo = 0;
    for (const auto& par : conteoMeses) {
        int mes = par.first;
        int conteo = par.second;
        if (conteo > maxConteo || (conteo == maxConteo && mes > maxMes)) {
            maxMes = mes;
            maxConteo = conteo;
        }
    }
    return maxMes;
}

// Método para obtener el año más frecuente
int Calendario::anyoMasFrecuente() const {
    if (eventos.empty()) {
        return -2;
    }
    std::unordered_map<int, int> conteoAnyos;
    for (const auto& par : eventos) {
        int anyo = par.first.getAnyo();
        conteoAnyos[anyo]++;
    }
    // Encontrar el año con mayor frecuencia
    int maxAnyo = -1;
    int maxConteo = 0;
    for (const auto& par : conteoAnyos) {
        int anyo = par.first;
        int conteo = par.second;
        if (conteo > maxConteo || (conteo == maxConteo && anyo > maxAnyo)) {
            maxAnyo = anyo;
            maxConteo = conteo;
        }
    }
    return maxAnyo;
}