#include "Evento.h"

// Constructor por defecto
Evento::Evento()
    : fecha(1, 1, 1900), titulo("sin título"), descripcion(""), categoria(-1) {}

// Constructor sobrecargado
Evento::Evento(const Fecha& f, const string& t, const string& d, int c)
    : fecha(f),
      titulo(t.empty() ? "sin título" : t),
      descripcion(d),
      categoria(c < -1 ? -1 : c) {}

// Constructor de copia
Evento::Evento(const Evento& e)
    : fecha(e.fecha),
      titulo(e.titulo),
      descripcion(e.descripcion),
      categoria(e.categoria) {}

// Operador de asignación
Evento& Evento::operator=(const Evento& e) {
    if (this != &e) {
        fecha = e.fecha;
        titulo = e.titulo;
        descripcion = e.descripcion;
        categoria = e.categoria;
    }
    return *this;
}

// Destructor
Evento::~Evento() {
    fecha = Fecha(1, 1, 1900);
    titulo = "sin título";
    descripcion = "";
    categoria = 0;
}

// Operador de igualdad
bool Evento::operator==(const Evento& e) const {
    return (fecha == e.fecha) &&
           (titulo == e.titulo) &&
           (descripcion == e.descripcion) &&
           (categoria == e.categoria);
}

// Operador de desigualdad
bool Evento::operator!=(const Evento& e) const {
    return !(*this == e);
}

// Getters
Fecha Evento::getFecha() const {
    return fecha;
}

string Evento::getTitulo() const {
    return titulo;
}

string Evento::getDescripcion() const {
    return descripcion;
}

int Evento::getCategoria() const {
    return categoria;
}

// Setters
void Evento::setFecha(const Fecha& f) {
    fecha = f;
}

void Evento::setTitulo(const string& t) {
    titulo = t.empty() ? "sin título" : t;
}

void Evento::setDescripcion(const string& d) {
    descripcion = d;
}

void Evento::setCategoria(int c) {
    categoria = (c < -1) ? -1 : c;
}

// Método para convertir a cadena
string Evento::aCadena(const vector<string>& categorias) const {
    // Obtener la representación de la fecha en formato largo con día de la semana
    string fechaStr = fecha.aCadena(true, true);

    // Obtener la descripción de la categoría
    string categoriaStr;
    if (categoria == -1) {
        categoriaStr = "";
    }
    else if (categoria >= 0 && categoria < static_cast<int>(categorias.size())) {
        categoriaStr = categorias[categoria];
    }
    else {
        categoriaStr = ""; // Manejo de índices fuera de rango
    }

    // Construir la cadena final según el formato especificado
    string resultado = fechaStr + ":" + titulo + "[" + categoriaStr + "]:" + descripcion;

    return resultado;
}