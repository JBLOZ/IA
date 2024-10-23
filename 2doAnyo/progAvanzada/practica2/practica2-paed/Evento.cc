#include "Evento.h"

Evento::Evento()
{
    this->descripcion = "sin descripción";
}

Evento::Evento(const Fecha& f, const string& d){

    this->fecha = f;
    if (d=="")
    {
        this->descripcion = "sin descripción";
    }
    else
    {
        this->descripcion = d;
    }
    

}

Evento::Evento(const Evento& e){
    this->fecha = e.fecha;
    this->descripcion = e.descripcion;

}

Evento& Evento::operator=(const Evento &e){

    this->fecha = e.fecha;
    this->descripcion = e.descripcion;
    return *this;
}

Evento::~Evento(){

    this->fecha = Fecha();
    this->descripcion = "sin descripción";

}

//Operador de comparación
bool Evento::operator==(const Evento &e) const{

    return(this->fecha == e.fecha and this->descripcion == e.descripcion);

}

//Operador de comparación
bool Evento::operator!=(const Evento &e) const{
    return(this->fecha != e.fecha || this->descripcion != e.descripcion);
}
//Operador de comparación
bool Evento::operator<(const Evento &e) const{
    return (this->fecha < e.fecha);
}

//Operador de comparación
bool Evento::operator>(const Evento &e) const{
    return(this->fecha > e.fecha);
}

//Devuelve (una copia de) la fecha
Fecha Evento::getFecha() const{
    
    return this->fecha;
}

//Devuelve (una copia de) la descripción
string Evento::getDescripcion() const{

    return this->descripcion;
}

//Modifica la fecha
void Evento::setFecha(const Fecha& f){
    this->fecha = f;
}

//Modifica la descripción
bool Evento::setDescripcion(const string &d){   
    if(d == "")
    {
        this->descripcion = "sin descripción";
    }
    else
    {
        this->descripcion = d;
    }
    return true;
}