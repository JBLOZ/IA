#include <string>       // Biblioteca estándar para manejar cadenas de caracteres (std::string)
#include "Fecha.h"      // Archivo de cabecera que declara la clase Fecha
#include <iostream>     // Biblioteca estándar para operaciones de entrada y salida (std::cout, std::cin)

using namespace std;    // Uso del espacio de nombres estándar para evitar prefijos repetitivos

/*
    Implementación de la clase Fecha
    Este archivo contiene las definiciones de todos los métodos declarados en Fecha.h.
    Incluye métodos privados para la validación y cálculo de fechas, así como métodos públicos para manipular y obtener información de la fecha.
*/

/*
    Métodos Privados
    Los métodos privados son accesibles únicamente desde dentro de la clase.
    Sirven para encapsular la lógica interna que no debe ser expuesta al usuario de la clase.
*/

// Método que verifica si una fecha es válida según el día, mes y año proporcionados.
// Declarado como 'const' para garantizar que no modifica el estado del objeto.
bool Fecha::esFechaCorrecta(int dia, int mes, int anyo) const
{
    // Verificación básica de los rangos de año, mes y día
    if (anyo >= 1900 && mes >= 1 && mes <= 12 && dia >= 1)
    {
        // Llamada a otro método privado para verificar la validez del día en el mes y año específicos
        if (dia <= Fecha::calculaDiasMes(mes, anyo))
        {
            return true; // La fecha es válida
        }
    }
    return false; // La fecha no es válida
}

// Método que determina si un año es bisiesto.
// Declarado como 'const' para garantizar que no modifica el estado del objeto.
bool Fecha::esBisiesto(int a) const
{
    // Un año es bisiesto si es divisible por 4 y (no divisible por 100 o divisible por 400)
    return (a % 4 == 0 && (a % 100 != 0 || a % 400 == 0));
}

// Método que calcula el número de días en un mes específico, considerando si el año es bisiesto.
// Declarado como 'const' para garantizar que no modifica el estado del objeto.
int Fecha::calculaDiasMes(int m, int a) const
{
    switch (m)
    {
        case 1: case 3: case 5: case 7: case 8: case 10: case 12:
            return 31; // Meses con 31 días
        case 2:
            return esBisiesto(a) ? 29 : 28; // Febrero: 29 días si es bisiesto, sino 28
        case 4: case 6: case 9: case 11:
            return 30; // Meses con 30 días
        default:
            return -1; // Mes inválido
    }
}

// Método que retorna el nombre del mes en español basado en su número.
// Declarado como 'const' para garantizar que no modifica el estado del objeto.
string Fecha::nombreMes(int m) const
{
    switch (m)
    {
        case 1:  return "enero";
        case 2:  return "febrero";
        case 3:  return "marzo";
        case 4:  return "abril";
        case 5:  return "mayo";
        case 6:  return "junio";
        case 7:  return "julio";
        case 8:  return "agosto";
        case 9:  return "septiembre";
        case 10: return "octubre";
        case 11: return "noviembre";
        case 12: return "diciembre";
        default: return "mes incorrecto"; // Manejo de casos inválidos
    }
}

// Método que retorna el nombre del día de la semana en español basado en su número (0 = lunes, 6 = domingo).
// Declarado como 'const' para garantizar que no modifica el estado del objeto.
string Fecha::nombreDia(int d) const
{
    switch (d)
    {
        case 0: return "lunes";
        case 1: return "martes";
        case 2: return "miércoles";
        case 3: return "jueves";
        case 4: return "viernes";
        case 5: return "sábado";
        case 6: return "domingo";
        default: return "día incorrecto"; // Manejo de casos inválidos
    }
}

// Método que calcula el día de la semana para la fecha actual usando el algoritmo de Zeller.
// Declarado como 'const' para garantizar que no modifica el estado del objeto.
int Fecha::obtenerDiaSemana() const 
{
    int d = dia;   // Día del mes
    int m = mes;   // Mes del año
    int y = anyo;  // Año
    int f;         // Variable para almacenar el resultado del algoritmo

    // Ajuste de mes y año según el algoritmo de Zeller
    if (m < 3) 
    {
        m += 12; // Enero y febrero se consideran como los meses 13 y 14 del año anterior
        y -= 1;
    }

    int K = y % 100; // Año dentro del siglo (últimos dos dígitos)
    int J = y / 100; // Siglo (primeros dos dígitos)

    // Aplicación del algoritmo de Zeller
    f = d + (13 * (m + 1)) / 5 + K + (K / 4) + (J / 4) - 2 * J;
    f = (f + 5) % 7; // Ajuste para que 0 corresponda a lunes

    return f; // Retorna el día de la semana (0 = lunes, 6 = domingo)
}

/*
    Métodos Públicos
    Los métodos públicos son accesibles desde fuera de la clase y permiten interactuar con los objetos de la clase.
*/

// Constructor por defecto: inicializa la fecha a 1/1/1900 utilizando una lista de inicialización.
Fecha::Fecha() : dia(1), mes(1), anyo(1900) {}

// Constructor sobrecargado: inicializa la fecha con los valores proporcionados si son válidos; si no, establece a 1/1/1900.
Fecha::Fecha(int d, int m, int a)
{
    if (esFechaCorrecta(d, m, a))
    {
        dia = d;
        mes = m;
        anyo = a;
    }
    else
    {
        dia = 1;
        mes = 1;
        anyo = 1900; // Fecha por defecto en caso de valores inválidos
    }
}

// Constructor de copia: crea una nueva fecha copiando otra existente utilizando una lista de inicialización.
Fecha::Fecha(const Fecha &f) : dia(f.dia), mes(f.mes), anyo(f.anyo) {}

// Operador de asignación: asigna los valores de una fecha a otra si son válidos.
// Retorna una referencia al objeto asignado para permitir encadenamiento de asignaciones.
Fecha& Fecha::operator=(const Fecha &f)
{
    // Evita la autoasignación comprobando si el objeto no se está asignando a sí mismo
    if (this != &f && esFechaCorrecta(f.dia, f.mes, f.anyo))
    {
        dia = f.dia;
        mes = f.mes;
        anyo = f.anyo;
    }
    return *this; // Retorna una referencia al objeto asignado
}

// Método getter que obtiene el día de la fecha.
// Declarado como 'const' para garantizar que no modifica el estado del objeto.
int Fecha::getDia() const
{
    return dia;
}

// Método getter que obtiene el mes de la fecha.
// Declarado como 'const' para garantizar que no modifica el estado del objeto.
int Fecha::getMes() const
{
    return mes;
}

// Método getter que obtiene el año de la fecha.
// Declarado como 'const' para garantizar que no modifica el estado del objeto.
int Fecha::getAnyo() const
{
    return anyo;
}

// Método setter que modifica el día de la fecha si el nuevo día es válido.
// Retorna 'true' si la modificación fue exitosa, 'false' en caso contrario.
bool Fecha::setDia(int d)
{
    if (esFechaCorrecta(d, mes, anyo))
    {
        dia = d;
        return true; // Modificación exitosa
    }
    return false; // Modificación fallida por día inválido
}

// Método setter que modifica el mes de la fecha si el nuevo mes es válido.
// Retorna 'true' si la modificación fue exitosa, 'false' en caso contrario.
bool Fecha::setMes(int m)
{
    if (esFechaCorrecta(dia, m, anyo))
    {
        mes = m;
        return true; // Modificación exitosa
    }
    return false; // Modificación fallida por mes inválido
}
// Destructor de la clase Fecha
Fecha::~Fecha() {
    // Si no es necesario liberar recursos, el destructor puede estar vacío.
}

// Método setter que modifica el año de la fecha si el nuevo año es válido.
// Retorna 'true' si la modificación fue exitosa, 'false' en caso contrario.
bool Fecha::setAnyo(int a)
{
    if (esFechaCorrecta(dia, mes, a))
    {
        anyo = a;
        return true; // Modificación exitosa
    }
    return false; // Modificación fallida por año inválido
}

// Sobrecarga del operador de igualdad: compara si dos fechas son iguales.
// Declarado como 'const' para garantizar que no modifica el estado del objeto.
bool Fecha::operator==(const Fecha &f) const
{
    return (dia == f.dia && mes == f.mes && anyo == f.anyo);
}

// Sobrecarga del operador de desigualdad: compara si dos fechas son diferentes.
// Declarado como 'const' para garantizar que no modifica el estado del objeto.
bool Fecha::operator!=(const Fecha &f) const
{
    return !(*this == f); // Reutiliza el operador de igualdad para simplificar
}

// Sobrecarga del operador menor que: compara si una fecha es menor que otra.
bool Fecha::operator<(const Fecha &f) const 
{
    if (this->anyo < f.getAnyo()) 
    {
        return true;
    } 
    else if (this->anyo == f.getAnyo()) 
    {
        if (this->mes < f.mes) 
        {
            return true;
        } 
        else if (this->mes == f.mes) 
        {
            return this->dia < f.dia;
        }
    }
    return false;
}

// Sobrecarga del operador mayor que: compara si una fecha es mayor que otra.
bool Fecha::operator>(const Fecha &f) const 
{
    if (this->anyo > f.getAnyo()) 
    {
        return true;
    } 
    else if (this->anyo == f.getAnyo()) 
    {
        if (this->mes > f.mes) 
        {
            return true;
        } 
        else if (this->mes == f.mes) 
        {
            return this->dia > f.dia;
        }
    }
    return false;
}

// Método que incrementa (o decrementa) la fecha en un número específico de días.
// Maneja correctamente el cambio de mes y año, incluyendo años bisiestos.
// Retorna 'true' si la operación fue exitosa, 'false' en caso contrario.
bool Fecha::incrementaDias(int inc)
{
    int dias_incremento = dia + inc; // Calcula el nuevo día después del incremento
    int copia_dia = dia;             // Guarda una copia del día actual para posibles reversiones
    int copia_mes = mes;             // Guarda una copia del mes actual
    int copia_anyo = anyo;           // Guarda una copia del año actual

    if (inc > 0)
    {
        // Incremento positivo de días
        while (dias_incremento > calculaDiasMes(mes, anyo))
        {
            dias_incremento -= calculaDiasMes(mes, anyo); // Resta los días del mes actual
            if (mes == 12)
            {
                mes = 1;    // Si es diciembre, pasa a enero
                anyo += 1;  // Incrementa el año
            }
            else
            {
                mes += 1;    // Incrementa el mes
            }
        }
    }
    else if (inc < 0)
    {
        // Decremento negativo de días
        while (dias_incremento <= 0)
        {
            if (mes == 1)
            {
                mes = 12;    // Si es enero, pasa a diciembre del año anterior
                anyo -= 1;   // Decrementa el año
            }
            else
            {
                mes -= 1;    // Decrementa el mes
            }
            dias_incremento += calculaDiasMes(mes, anyo); // Suma los días del mes anterior
        }
    }

    dia = dias_incremento; // Actualiza el día con el nuevo valor

    // Verifica si la nueva fecha es válida
    if (esFechaCorrecta(dia, mes, anyo))
    {
        return true; // Operación exitosa
    }
    else
    {
        // Revertir los cambios si la nueva fecha no es válida
        dia = copia_dia;
        mes = copia_mes;
        anyo = copia_anyo;
        return false; // Operación fallida
    }
}

// Método que incrementa (o decrementa) la fecha en un número específico de meses.
// Maneja correctamente el cambio de año si el incremento excede los límites de los meses.
// Retorna 'true' si la operación fue exitosa, 'false' en caso contrario.
bool Fecha::incrementaMeses(int inc)
{
    int nuevo_mes = mes + inc; // Calcula el nuevo mes después del incremento
    int ajuste_anyo = 0;       // Variable para ajustar el año si el nuevo mes excede los límites

    // Ajusta el año según el número de meses incrementados
    while (nuevo_mes > 12)
    {
        nuevo_mes -= 12; // Resta 12 meses (un año)
        ajuste_anyo += 1; // Incrementa el ajuste de año
    }
    while (nuevo_mes < 1)
    {
        nuevo_mes += 12; // Suma 12 meses (un año)
        ajuste_anyo -= 1; // Decrementa el ajuste de año
    }

    int nuevo_anyo = anyo + ajuste_anyo; // Calcula el nuevo año

    // Verifica si la nueva fecha es válida
    if (esFechaCorrecta(dia, nuevo_mes, nuevo_anyo))
    {
        mes = nuevo_mes; // Actualiza el mes
        anyo = nuevo_anyo; // Actualiza el año
        return true; // Operación exitosa
    }

    return false; // Operación fallida
}

// Método que incrementa (o decrementa) la fecha en un número específico de años.
// Retorna 'true' si la operación fue exitosa, 'false' en caso contrario.
bool Fecha::incrementaAnyos(int inc)
{
    int nuevo_anyo = anyo + inc; // Calcula el nuevo año

    // Verifica si la nueva fecha es válida
    if (esFechaCorrecta(dia, mes, nuevo_anyo))
    {
        anyo = nuevo_anyo; // Actualiza el año
        return true; // Operación exitosa
    }

    return false; // Operación fallida
}

// Método que genera una representación en cadena de la fecha.
// Parámetros:
// - larga: si es verdadero, usa el formato "día de mes de año"; si es falso, usa "día/mes/año".
// - conDia: si es verdadero, incluye el nombre del día de la semana.
// Declarado como 'const' para garantizar que no modifica el estado del objeto.
string Fecha::aCadena(bool larga, bool conDia) const
{
    string resultado; // Variable para almacenar la representación en cadena
    int dia_semana = obtenerDiaSemana(); // Obtiene el día de la semana
    string nombre_dia = nombreDia(dia_semana); // Obtiene el nombre del día de la semana

    if (conDia)
    {
        resultado += nombre_dia + " "; // Añade el nombre del día de la semana si se requiere
    }

    if (larga)
    {
        // Formato largo: "martes 5 de abril de 2023"
        resultado += to_string(dia) + " de " + nombreMes(mes) + " de " + to_string(anyo);
    }
    else
    {
        // Formato corto: "5/4/2023"
        resultado += to_string(dia) + "/" + to_string(mes) + "/" + to_string(anyo);
    }

    return resultado; // Retorna la representación en cadena de la fecha
}