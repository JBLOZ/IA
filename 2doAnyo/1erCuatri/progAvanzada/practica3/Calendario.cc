#include "Calendario.h"
#include <algorithm>
#include <cctype>


Calendario::Calendario(){}

Calendario::Calendario(const Calendario& c) {
    eventos = c.eventos;
    indiceTitulo = c.indiceTitulo;
    historialInserciones = c.historialInserciones;
    historialBorrados = c.historialBorrados;
    freqCat = c.freqCat;
    freqDia = c.freqDia;
    freqMes = c.freqMes;
    freqAny = c.freqAny;
}

Calendario& Calendario::operator=(const Calendario &c) {
    if(this!=&c){
        eventos = c.eventos;
        indiceTitulo = c.indiceTitulo;
        historialInserciones = c.historialInserciones;
        historialBorrados = c.historialBorrados;
        freqCat = c.freqCat;
        freqDia = c.freqDia;
        freqMes = c.freqMes;
        freqAny = c.freqAny;
    }
    return *this;
}

Calendario::~Calendario(){}

void Calendario::incrementarFrecuencias(const Evento &e){
   freqCat[e.getCategoria()]++;
   freqDia[e.getFecha().getDia()]++;
   freqMes[e.getFecha().getMes()]++;
   freqAny[e.getFecha().getAnyo()]++;
}
void Calendario::decrementarFrecuencias(const Evento &e){
   freqCat[e.getCategoria()]--;
   if(freqCat[e.getCategoria()]<=0) freqCat.erase(e.getCategoria());
   freqDia[e.getFecha().getDia()]--;
   if(freqDia[e.getFecha().getDia()]<=0) freqDia.erase(e.getFecha().getDia());
   freqMes[e.getFecha().getMes()]--;
   if(freqMes[e.getFecha().getMes()]<=0) freqMes.erase(e.getFecha().getMes());
   freqAny[e.getFecha().getAnyo()]--;
   if(freqAny[e.getFecha().getAnyo()]<=0) freqAny.erase(e.getFecha().getAnyo());
}

bool Calendario::insertarEvento(const Evento& ev) {
    Fecha f = ev.getFecha();
    if(eventos.find(f)!=eventos.end()) {
        // ya existe evento en esa fecha
        return false;
    }
    // insertar
    eventos[f]=ev;
    indiceTitulo.insert({ev.getTitulo(), f});
    incrementarFrecuencias(ev);
    // Guardar en historial inserciones
    historialInserciones.push(ev);
    return true;
}

bool Calendario::eliminarEvento(const Fecha& f) {
    auto it = eventos.find(f);
    if(it==eventos.end()) return false;
    Evento e = it->second;
    // borrar
    eventos.erase(it);

    // borrar del índice de título
    // necesitamos buscar todas las entradas con ese título y borrar la que coincida en fecha
    auto range = indiceTitulo.equal_range(e.getTitulo());
    for(auto i = range.first; i!=range.second; i++){
        if(i->second==f){
            indiceTitulo.erase(i);
            break;
        }
    }

    decrementarFrecuencias(e);
    // Guardar en historial borrados
    historialBorrados.push(e);
    return true;
}

bool Calendario::comprobarEvento(const Fecha& f) const {
    return (eventos.find(f)!=eventos.end());
}

Evento Calendario::obtenerEvento(const Fecha& f) const {
    auto it=eventos.find(f);
    if(it==eventos.end()) {
        // no hay evento, devolver evento por defecto del enunciado
        return Evento();
    }
    return it->second;
}

string Calendario::aCadena(const vector<string>& cats) const {
    // un evento por línea, en orden cronológico
    // Formato: fecha_larga_con_dia:titulo[categoria]:descripcion
    // sin salto de línea final extra
    string res;
    for(auto it=eventos.begin(); it!=eventos.end(); it++){
        if(it!=eventos.begin()) res+="\n";
        res += it->second.aCadena(cats);
    }
    return res;
}

void Calendario::deshacerInsercion() {
    // elimina el evento añadido en la última inserción exitosa
    if(historialInserciones.empty()) return;
    Evento e = historialInserciones.top();
    historialInserciones.pop();
    // eliminar del calendario sin registrar en historial borrados (ya que es un deshacer)
    auto it=eventos.find(e.getFecha());
    if(it!=eventos.end()){
        // antes de borrar, quitar del indice titulo y freq
        Fecha f = e.getFecha();
        // índice titulo
        auto range = indiceTitulo.equal_range(e.getTitulo());
        for(auto i=range.first; i!=range.second; i++){
            if(i->second==f) { indiceTitulo.erase(i); break; }
        }
        decrementarFrecuencias(e);
        eventos.erase(it);
    }
}

void Calendario::deshacerBorrado() {
    // volver a insertar el evento borrado en el último borrado exitoso
    if(historialBorrados.empty()) return;
    Evento e = historialBorrados.top();
    historialBorrados.pop();
    // reinsertar sin añadir al historial de inserciones
    if(eventos.find(e.getFecha())==eventos.end()){
        eventos[e.getFecha()]=e;
        indiceTitulo.insert({e.getTitulo(), e.getFecha()});
        incrementarFrecuencias(e);
    }
}

string Calendario::aCadenaPorTitulo(const string& t, const vector<string>& cats) const {
    // Buscamos en indiceTitulo
    // Debemos devolver en orden cronológico
    // Filtramos sólo las fechas con ese título
    vector<Fecha> fechas;
    auto range = indiceTitulo.equal_range(t);
    for(auto it=range.first; it!=range.second; it++){
        fechas.push_back(it->second);
    }
    if(fechas.empty()) return "";
    // Ordenar fechas
    sort(fechas.begin(), fechas.end());
    // imprimir eventos
    string res;
    for(size_t i=0;i<fechas.size();i++){
        if(i>0) res+="\n";
        res += eventos.at(fechas[i]).aCadena(cats);
    }
    return res;
}

int Calendario::masFrecuente(const map<int,int> &m, int vacioValue) const {
    if(m.empty()) return vacioValue;
    int maxFreq = -1; int val = -1;
    for(auto &par: m) {
        if(par.second>maxFreq || (par.second==maxFreq && par.first>val)) {
            maxFreq=par.second; val=par.first;
        }
    }
    return val;
}

int Calendario::categoriaMasFrecuente() const {
    return masFrecuente(freqCat,-2);
}
int Calendario::diaMasFrecuente() const {
    return masFrecuente(freqDia,-2);
}
int Calendario::mesMasFrecuente() const {
    return masFrecuente(freqMes,-2);
}
int Calendario::anyoMasFrecuente() const {
    return masFrecuente(freqAny,-2);
}


vector<Evento> Calendario::buscarEventosPorPalabraClave(const string& palabraClave) const {

    vector<Evento> resultados;
    string clave = palabraClave;

    transform(clave.begin(), clave.end(), clave.begin(), ::tolower);

    
    for (const auto& par : eventos) {
        const Evento& evento = par.second;

        
        string titulo = evento.getTitulo();
        string descripcion = evento.getDescripcion();

        transform(titulo.begin(), titulo.end(), titulo.begin(), ::tolower);
        transform(descripcion.begin(), descripcion.end(), descripcion.begin(), ::tolower);

        
        if (titulo.find(clave) != string::npos || descripcion.find(clave) != string::npos) {
            resultados.push_back(evento);
        }
    }

    return resultados;
}


vector<Evento> Calendario::buscarEventosPorTituloExacto(const string& tituloExacto) const {
    vector<Evento> resultados;

    // Iterar sobre todos los eventos en el mapa
    for (const auto& par : eventos) {
        const Evento& evento = par.second;

        // Comprobar coincidencia exacta del título
        if (evento.getTitulo() == tituloExacto) {
            resultados.push_back(evento); // Añadir a resultados
        }
    }

    return resultados;
}