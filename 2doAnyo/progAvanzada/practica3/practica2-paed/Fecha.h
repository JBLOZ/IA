#ifndef FECHA_H
#define FECHA_H

#include <string>        // Biblioteca estándar para manejar cadenas de caracteres (std::string)

using namespace std;     // Utiliza el espacio de nombres estándar para evitar prefijos repetitivos

/*
    Guardas de inclusión (Include Guards)
    -------------------------------------
    Las guardas de inclusión previenen que el contenido del archivo de cabecera se
    incluya múltiples veces durante la compilación, lo que podría causar errores de
    redefinición. Se utilizan preprocesadores para definir una macro única que
    controla la inclusión del contenido.

    #ifndef FECHA_H
        Verifica si la macro FECHA_H no ha sido definida previamente.
    #define FECHA_H
        Define la macro FECHA_H para que futuras inclusiones de este archivo
        no vuelvan a incluir su contenido.
    ...
    #endif
        Marca el final de la guardia de inclusión.
*/
 
class Fecha {
private:
    // **Atributos Privados**
    // Los atributos privados solo son accesibles desde dentro de la clase.
    // Esto es parte del principio de encapsulamiento, que protege los datos
    // internos de accesos no autorizados o modificaciones indebidas.
    int dia, mes, anyo; // Representan el día, mes y año de la fecha.

    // **Funciones Auxiliares Privadas**
    // Estas funciones ayudan a mantener la integridad de los datos y realizan
    // operaciones internas que no deben ser expuestas al usuario de la clase.
    
    // Verifica si una fecha específica es válida.
    // Parámetros: día, mes, año.
    // Retorna: true si la fecha es válida, false en caso contrario.
    bool esFechaCorrecta(int, int, int) const;

    // Determina si un año es bisiesto.
    // Parámetro: año.
    // Retorna: true si el año es bisiesto, false en caso contrario.
    bool esBisiesto(int) const;

    // Calcula el número de días en un mes específico, considerando si el año es bisiesto.
    // Parámetros: mes, año.
    // Retorna: número de días en el mes, o -1 si el mes es inválido.
    int calculaDiasMes(int, int) const;

    // Calcula el día de la semana para la fecha actual.
    // Retorna: un entero representando el día de la semana (0 = lunes, 6 = domingo).
    int obtenerDiaSemana() const;

public:
    // **Constructores Públicos**
    // Los constructores permiten la creación de objetos de la clase Fecha.
    
    // Constructor por defecto
    // Inicializa una fecha con valores predeterminados (1/1/1900).
    Fecha();
    
    // Constructor sobrecargado
    // Permite inicializar una fecha con valores específicos proporcionados como parámetros.
    // Parámetros: día, mes, año.
    Fecha(int dia, int mes, int anyo);
    
    // Constructor de copia
    // Crea una nueva instancia de Fecha copiando los valores de otra instancia existente.
    // Parámetro: referencia constante a otro objeto Fecha.
    Fecha(const Fecha &);
    
    // **Destructor Público**
    // El destructor se invoca automáticamente cuando un objeto Fecha deja de existir.
    // Es útil para liberar recursos si la clase maneja memoria dinámica u otros recursos.
    ~Fecha();

    // **Operador de Asignación**
    // Sobrecarga el operador de asignación (=) para copiar los valores de un objeto Fecha a otro.
    // Parámetro: referencia constante a otro objeto Fecha.
    // Retorna: referencia al objeto Fecha asignado (*this).
    Fecha& operator=(const Fecha &);
    
    // **Operadores de Comparación**
    // Permiten comparar dos objetos Fecha usando operadores estándar (==, !=).
    
    // Sobrecarga del operador de igualdad (==)
    // Compara si dos fechas son exactamente iguales (mismo día, mes y año).
    // Parámetro: referencia constante a otro objeto Fecha.
    // Retorna: true si las fechas son iguales, false en caso contrario.
    bool operator==(const Fecha &) const;

    // Sobrecarga del operador de desigualdad (!=)
    // Compara si dos fechas son diferentes.
    // Parámetro: referencia constante a otro objeto Fecha.
    // Retorna: true si las fechas son diferentes, false en caso contrario.
    bool operator!=(const Fecha &) const;

    //Operador de comparación
   bool operator<(const Fecha &) const;
   
   //Operador de comparación
   bool operator>(const Fecha &) const;
    
    // **Métodos Getters**
    // Permiten acceder a los valores de los atributos privados de forma controlada.
    
    // Obtiene el día de la fecha.
    // Retorna: valor entero del día.
    int getDia() const;
    
    // Obtiene el mes de la fecha.
    // Retorna: valor entero del mes.
    int getMes() const;
    
    // Obtiene el año de la fecha.
    // Retorna: valor entero del año.
    int getAnyo() const;
    
    // **Métodos Setters**
    // Permiten modificar los valores de los atributos privados de forma controlada,
    // asegurando que los nuevos valores mantengan la integridad del objeto.
    
    // Modifica el día de la fecha.
    // Parámetro: nuevo día.
    // Retorna: true si la modificación fue exitosa, false si la fecha resultante es inválida.
    bool setDia(int);
    
    // Modifica el mes de la fecha.
    // Parámetro: nuevo mes.
    // Retorna: true si la modificación fue exitosa, false si la fecha resultante es inválida.
    bool setMes(int);
    
    // Modifica el año de la fecha.
    // Parámetro: nuevo año.
    // Retorna: true si la modificación fue exitosa, false si la fecha resultante es inválida.
    bool setAnyo(int);
    
    // **Métodos para Incrementar o Decrementar la Fecha**
    // Permiten ajustar la fecha añadiendo o restando días, meses o años.
    
    // Incrementa (o decrementa) la fecha en un número específico de días.
    // Parámetro: número de días a incrementar (positivo) o decrementar (negativo).
    // Retorna: true si la operación fue exitosa, false en caso contrario.
    bool incrementaDias(int);
    
    // Incrementa (o decrementa) la fecha en un número específico de meses.
    // Parámetro: número de meses a incrementar (positivo) o decrementar (negativo).
    // Retorna: true si la operación fue exitosa, false en caso contrario.
    bool incrementaMeses(int);
    
    // Incrementa (o decrementa) la fecha en un número específico de años.
    // Parámetro: número de años a incrementar (positivo) o decrementar (negativo).
    // Retorna: true si la operación fue exitosa, false en caso contrario.
    bool incrementaAnyos(int);
    
    // **Método para Obtener una Representación en Cadena de la Fecha**
    // Permite obtener una representación textual de la fecha, en diferentes formatos.
    
    // Genera una cadena que representa la fecha.
    // Parámetros:
    // - larga: si es true, utiliza un formato extendido (ej. "5 de abril de 2023");
    //          si es false, utiliza un formato corto (ej. "5/4/2023").
    // - conDia: si es true, incluye el nombre del día de la semana (ej. "martes 5 de abril de 2023");
    //           si es false, solo incluye la fecha sin el día de la semana.
    // Retorna: cadena de caracteres que representa la fecha en el formato solicitado.
    string aCadena(bool larga, bool conDia) const;
    
    // **Funciones para Obtener el Nombre del Mes y del Día de la Semana**
    // Facilitan la conversión de números a sus nombres correspondientes en español.
    
    // Retorna el nombre del mes en español basado en su número.
    // Parámetro: número del mes (1-12).
    // Retorna: cadena con el nombre del mes, o "mes incorrecto" si el número no es válido.
    string nombreMes(int m) const;
    
    // Retorna el nombre del día de la semana en español basado en su número.
    // Parámetro: número del día de la semana (0 = lunes, 6 = domingo).
    // Retorna: cadena con el nombre del día, o "día incorrecto" si el número no es válido.
    string nombreDia(int d) const;
};

#endif // FECHA_H
