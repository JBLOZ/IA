#include "Evento.h"

Evento::Evento() {
    fecha = Fecha(1,1,1900);
    titulo = "sin título";
    descripcion = "";
    categoria = -1;
}

Evento::Evento(const Fecha& f, const string& t, const string& desc, int cat) {
    fecha = f;
    if(t.empty()) titulo="sin título"; else titulo=t;
    descripcion=desc;
    if(cat< -1) categoria=-1; else categoria=cat;
}

Evento::Evento(const Evento& e) {
    fecha = e.fecha;
    titulo = e.titulo;
    descripcion = e.descripcion;
    categoria = e.categoria;
}

Evento& Evento::operator=(const Evento &e) {
    if(this!=&e){
        fecha = e.fecha;
        titulo = e.titulo;
        descripcion = e.descripcion;
        categoria = e.categoria;
    }
    return *this;
}

Evento::~Evento(){
    fecha = Fecha(1,1,1900);
    titulo = "sin título";
    descripcion = "";
    categoria = 0;
}

bool Evento::operator==(const Evento &e) const {
    return (fecha==e.fecha && titulo==e.titulo && descripcion==e.descripcion && categoria==e.categoria);
}

bool Evento::operator!=(const Evento &e) const {
    return !(*this==e);
}

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

void Evento::setFecha(const Fecha& f){
    fecha = f;
}
void Evento::setTitulo(const string &t){
    if(t.empty()) titulo="sin título"; else titulo=t;
}
void Evento::setDescripcion(const string &d){
    descripcion=d;
}
void Evento::setCategoria(int c){
    if(c< -1) categoria=-1; else categoria=c;
}

string Evento::aCadena(const vector<string>& categorias) const {
    // fecha larga con día: "lunes 9 de septiembre de 2024"
    string f = fecha.aCadena(true,true);
    string catStr="";
    if(categoria!=-1 && categoria<(int)categorias.size()) catStr=categorias[categoria];
    // Formato: fecha:titulo[catStr]:descripcion
    return f+":"+titulo+"["+catStr+"]:"+descripcion;
}
