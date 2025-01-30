#ifndef FECHA_H
#define FECHA_H

#include <string>
using namespace std;

class Fecha{
   private:
   int dia, mes, anyo;
   bool esFechaCorrecta(int, int, int) const;
   bool esBisiesto(int) const;
   int calculaDiasMes(int, int) const;
   int obtenerDiaSemana() const;
   string nombreMes(int) const;
   string nombreDia(int) const;

   public:
   //Constructor por defecto: inicializa la fecha a 1/1/1900
   Fecha();
   //Constructor sobrecargado: inicializa la fecha según los parámetros
   Fecha(int dia,int mes,int anyo);
   //Constructor de copia
   Fecha(const Fecha &);
   //Destructor: pone la fecha a 1/1/1900
   ~Fecha();
   //Operador de asignación
   Fecha& operator=(const Fecha &);

   bool operator==(const Fecha &) const;
   bool operator!=(const Fecha &) const;
   bool operator<(const Fecha &) const;
   bool operator>(const Fecha &) const;

   int getDia() const;
   int getMes() const;
   int getAnyo() const;

   bool setDia(int);
   bool setMes(int);
   bool setAnyo(int);

   bool incrementaDias(int );
   bool incrementaMeses(int );
   bool incrementaAnyos(int );

   //Devuelve una representación como cadena de la fecha
   // larga = true -> formato largo "lunes 9 de septiembre de 2024"
   // conDia = true -> incluir el nombre del día de la semana
   string aCadena(bool larga, bool conDia) const;
};

#endif

#ifndef EVENTO_H
#define EVENTO_H

#include<string>
#include<vector>
using namespace std;

class Evento{
private:
   Fecha fecha;
   string titulo;
   string descripcion;
   int categoria;

public:
   //Constructor por defecto: fecha 1/1/1900, titulo "sin título", descr vacía, cat -1
   Evento();
   //Constructor sobrecargado
   Evento(const Fecha&, const string&, const string&, int);
   //Constructor de copia
   Evento(const Evento&);
   //Operador de asignación
   Evento& operator=(const Evento &);
   //Destructor: pone la fecha a 1/1/1900, el título a "sin título", descr = "", cat=0
   ~Evento();

   bool operator==(const Evento &) const;
   bool operator!=(const Evento &) const;

   Fecha getFecha() const;
   string getTitulo() const;
   string getDescripcion() const;
   int getCategoria() const;

   void setFecha(const Fecha& );
   void setTitulo(const string &);
   void setDescripcion(const string &);
   void setCategoria(int);

   //Convierte en cadena
   //Formato: "lunes 9 de septiembre de 2024:Título[categoría_en_texto]:Descripción"
   //Si cat=-1, categoría_en_texto=""
   string aCadena(const vector<string>&) const;
};

#endif

#ifndef CALENDARIO_H
#define CALENDARIO_H

#include <string>
#include <vector>
#include <map>
#include <stack>
#include <map>
#include <iostream>
#include <algorithm>
#include <unordered_map>

using namespace std;

class Calendario{
private:
   // Map principal: Fecha->Evento
   map<Fecha,Evento> eventos;
   // Para búsqueda por título: Titulo->(múltiples fechas)
   multimap<string,Fecha> indiceTitulo;

   // Estructuras para deshacer
   // Para deshacer inserciones: almacenamos el evento insertado
   stack<Evento> historialInserciones;
   // Para deshacer borrados: almacenamos el evento borrado
   stack<Evento> historialBorrados;

   // Frecuencias
   // categoría->frecuencia
   map<int,int> freqCat;
   // día->frecuencia
   map<int,int> freqDia;
   // mes->frecuencia
   map<int,int> freqMes;
   // año->frecuencia
   map<int,int> freqAny;

   void incrementarFrecuencias(const Evento &e);
   void decrementarFrecuencias(const Evento &e);
   int masFrecuente(const map<int,int> &m, int vacioValue) const;

public:
   Calendario();
   Calendario(const Calendario&);
   Calendario& operator=(const Calendario &);
   ~Calendario();

   bool insertarEvento(const Evento&);
   bool eliminarEvento(const Fecha&);
   bool comprobarEvento(const Fecha&) const;
   Evento obtenerEvento(const Fecha&) const;
   string aCadena(const vector<string>&) const;

   void deshacerInsercion();
   void deshacerBorrado();

   string aCadenaPorTitulo(const string&, const vector<string>&) const;

   int categoriaMasFrecuente() const;
   int diaMasFrecuente() const;
   int mesMasFrecuente() const;
   int anyoMasFrecuente() const;

   vector<Evento> buscarEventosPorPalabraClave(const string& palabraClave) const;
   vector<Evento> buscarEventosPorTituloExacto(const string& tituloExacto) const;

};

#endif

#include <iostream>
#include <string>
#include <vector>

using namespace std;

void leerCategorias(vector<string>& categorias) {
    string line;
    while (getline(cin, line) && line != "[FIN_CATEGORIAS]") {
        categorias.push_back(line);
    }
}

void procesarInsertarEvento(Calendario& cal) {
    int d, m, a, cat;
    string t, desc;
    cin >> d >> m >> a >> t >> desc >> cat;
    for (auto& c : t) if (c == '_') c = ' ';
    for (auto& c : desc) if (c == '_') c = ' ';
    Evento ev(Fecha(d, m, a), t, desc, cat);
    cout << (cal.insertarEvento(ev) ? 1 : 0) << '\n';
}

void procesarEliminarEvento(Calendario& cal) {
    int d, m, a;
    cin >> d >> m >> a;
    cout << (cal.eliminarEvento(Fecha(d, m, a)) ? 1 : 0) << '\n';
}

void procesarComprobarEvento(Calendario& cal) {
    int d, m, a;
    cin >> d >> m >> a;
    cout << (cal.comprobarEvento(Fecha(d, m, a)) ? 1 : 0) << '\n';
}

void procesarObtenerEvento(Calendario& cal, const vector<string>& categorias) {
    int d, m, a;
    cin >> d >> m >> a;
    Evento ev = cal.obtenerEvento(Fecha(d, m, a));
    cout << ev.aCadena(categorias) << '\n';
}

void procesarCadena(Calendario& cal, const vector<string>& categorias) {
    string s = cal.aCadena(categorias);
    if (!s.empty()) cout << s << '\n';
}

void procesarCadenaPorTitulo(Calendario& cal, const vector<string>& categorias) {
    string t;
    cin >> t;
    for (auto& c : t) if (c == '_') c = ' ';
    string s = cal.aCadenaPorTitulo(t, categorias);
    if (!s.empty()) cout << s << '\n';
}

void procesarConsultaFrecuencia(Calendario& cal, const string& tipo) {
    if (tipo == "categoriaMasFrecuente") cout << cal.categoriaMasFrecuente() << '\n';
    else if (tipo == "diaMasFrecuente") cout << cal.diaMasFrecuente() << '\n';
    else if (tipo == "mesMasFrecuente") cout << cal.mesMasFrecuente() << '\n';
    else if (tipo == "anyoMasFrecuente") cout << cal.anyoMasFrecuente() << '\n';
}

// Ejemplo de nuevo método en el examen
void procesarMetodoNuevo(Calendario& cal, const vector<string>& categorias) {
    // Este método se deberá implementar en función de lo que pidan en el examen
    // Aquí puedes leer parámetros específicos del nuevo método y llamar a la lógica correspondiente
    string t;
    cin >> t;
    for (auto& c : t) if (c == '_') c = ' ';
    vector<Evento> resultados = cal.buscarEventosPorPalabraClave(t);
    // Implementar la lógica para interactuar con cal
    if (!resultados.empty()) {
        for (const auto& e : resultados) {
            cout << e.aCadena(categorias) << '\n';
        }
    }
    else {
        cout << "No hay eventos con la palabra clave " << t << '\n';
    }
    
}

void procesarComando(Calendario& cal, const string& comando, const vector<string>& categorias) {
    if (comando == "insertarEvento") {
        procesarInsertarEvento(cal);
    } else if (comando == "eliminarEvento") {
        procesarEliminarEvento(cal);
    } else if (comando == "comprobarEvento") {
        procesarComprobarEvento(cal);
    } else if (comando == "obtenerEvento") {
        procesarObtenerEvento(cal, categorias);
    } else if (comando == "aCadena") {
        procesarCadena(cal, categorias);
    } else if (comando == "aCadenaPorTitulo") {
        procesarCadenaPorTitulo(cal, categorias);
    } else if (comando == "categoriaMasFrecuente" || comando == "diaMasFrecuente" || comando == "mesMasFrecuente" || comando == "anyoMasFrecuente") {
        procesarConsultaFrecuencia(cal, comando);
    } else if (comando == "deshacerInsercion") {
        cal.deshacerInsercion();
    } else if (comando == "deshacerBorrado") {
        cal.deshacerBorrado();
    } else if (comando == "metodoNuevo") { // Comando para el examen
        procesarMetodoNuevo(cal, categorias);
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<string> categorias;
    leerCategorias(categorias);

    Calendario cal;
    string comando;
    while (cin >> comando && comando != "[FIN]") {
        procesarComando(cal, comando, categorias);
    }

    return 0;
}

#include <iostream>
using namespace std;

bool Fecha::esFechaCorrecta(int d,int m,int a) const {
    if(a<1900 || m<1 || m>12 || d<1) return false;
    return (d<=calculaDiasMes(m,a));
}

bool Fecha::esBisiesto(int a) const {
    return ((a%4==0 && a%100!=0) || (a%400==0));
}

int Fecha::calculaDiasMes(int m, int a) const {
    switch (m){
        case 1:case 3:case 5:case 7:case 8:case 10:case 12:return 31;
        case 4:case 6:case 9:case 11:return 30;
        case 2:return (esBisiesto(a)?29:28);
    }
    return -1;
}

string Fecha::nombreMes(int m) const {
    string meses[12]={"enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"};
    if(m<1||m>12) return "mes incorrecto";
    return meses[m-1];
}

string Fecha::nombreDia(int d) const {
    // d: 0=lunes,1=martes,...6=domingo
    string dias[7]={"lunes","martes","miércoles","jueves","viernes","sábado","domingo"};
    if(d<0||d>6) return "día incorrecto";
    return dias[d];
}

int Fecha::obtenerDiaSemana() const {
    int d = dia;
    int m = mes;
    int y = anyo;

    // Si el mes es enero o febrero, se considera como el mes 13 y 14 del año anterior
    if(m < 3) {
        m += 12;
        y -= 1;
    }

    int K = y % 100;
    int J = y / 100;

    // Fórmula de Zeller
    int f = d + (13*(m+1))/5 + K + K/4 + J/4 + 5*J;
    f = f % 7; 

    // Ahora f=0 representa sábado
    // Queremos 0=lunes,1=martes,...,6=domingo
    // Mapeo actual (f=0 sabado):
    // f:0=sat,1=sun,2=mon,3=tue,4=wed,5=thu,6=fri
    // Queremos:0=lun,1=mar,2=mié,3=jue,4=vie,5=sáb,6=dom
    // Observando el patrón:
    // mon(2 zeller) -> 0 nuestro
    // Para alinear: nuevo_indice = (f + 5) % 7 (tal como estaba antes)
    // Comprobamos: f=0(sat) -> (0+5)%7=5=sábado (correcto)
    // f=1(sun) -> (1+5)%7=6=domingo (correcto)
    // f=2(mon) -> (2+5)%7=0=lunes (correcto)
    // y así sucesivamente.

    return (f+5)%7;
}

Fecha::Fecha(){
    dia=1;mes=1;anyo=1900;
}

Fecha::Fecha(int d,int m,int a){
    if(esFechaCorrecta(d,m,a)) {
        dia=d;mes=m;anyo=a;
    } else {
        dia=1;mes=1;anyo=1900;
    }
}

Fecha::Fecha(const Fecha &f){
    if(esFechaCorrecta(f.dia,f.mes,f.anyo)) {
        dia=f.dia;mes=f.mes;anyo=f.anyo;
    } else {
        dia=1;mes=1;anyo=1900;
    }
}

Fecha::~Fecha(){
    dia=1;mes=1;anyo=1900;
}

Fecha& Fecha::operator=(const Fecha &f){
    if(this!=&f){
        if(esFechaCorrecta(f.dia,f.mes,f.anyo)) {
            dia=f.dia;mes=f.mes;anyo=f.anyo;
        } else {
            dia=1;mes=1;anyo=1900;
        }
    }
    return *this;
}

int Fecha::getDia() const {return dia;}
int Fecha::getMes() const {return mes;}
int Fecha::getAnyo() const{return anyo;}

bool Fecha::setDia(int d) {
    if(esFechaCorrecta(d,mes,anyo)){dia=d;return true;}
    return false;
}
bool Fecha::setMes(int m) {
    if(esFechaCorrecta(dia,m,anyo)){mes=m;return true;}
    return false;
}
bool Fecha::setAnyo(int a) {
    if(esFechaCorrecta(dia,mes,a)){anyo=a;return true;}
    return false;
}

bool Fecha::operator==(const Fecha &f) const {
    return (dia==f.dia && mes==f.mes && anyo==f.anyo);
}
bool Fecha::operator!=(const Fecha &f) const {
    return !(*this==f);
}
bool Fecha::operator<(const Fecha &f) const {
    if(anyo<f.anyo) return true;
    if(anyo>f.anyo) return false;
    if(mes<f.mes) return true;
    if(mes>f.mes) return false;
    return (dia<f.dia);
}
bool Fecha::operator>(const Fecha &f) const {
    return f<*this;
}

// Zeller’s congruence (modificación para días del 0 al 6)
// 0=Saturday, 1=Sunday, 2=Monday, ..., 6=Friday.


bool Fecha::incrementaDias(int inc) {
    // Convertir fecha a días desde 1/1/1900
    int totalDays = 0;
    // Contamos años completos
    for (int year=1900; year<anyo; year++) {
        totalDays += (esBisiesto(year)?366:365);
    }
    // Añadimos meses del año actual
    for (int mm=1; mm<mes; mm++) {
        totalDays += calculaDiasMes(mm, anyo);
    }
    // Añadimos los días del mes actual (dia-1 porque el 1 de enero de 1900 sería día 0)
    totalDays += (dia-1);

    // Incrementamos
    totalDays += inc;
    if (totalDays<0) {
        // No soportamos fechas antes de 1/1/1900 en este caso, puedes decidir qué hacer
        return false;
    }

    // Convertir de vuelta a fecha
    int yy=1900;
    while (true) {
        int dyear = esBisiesto(yy)?366:365;
        if (totalDays < dyear) break;
        totalDays -= dyear;
        yy++;
    }

    int mm=1;
    while (true) {
        int dmes = calculaDiasMes(mm, yy);
        if (totalDays < dmes) break;
        totalDays -= dmes;
        mm++;
    }

    int dd = totalDays + 1; // sumamos 1 porque empezamos en 0
    if (!esFechaCorrecta(dd, mm, yy)) return false;
    dia=dd; mes=mm; anyo=yy;
    return true;
}


bool Fecha::incrementaMeses(int inc) {
    int mm=mes+inc;int aa=anyo;int dd=dia;
    while(mm>12){mm-=12;aa++;}
    while(mm<1){mm+=12;aa--;}
    if(dd>calculaDiasMes(mm,aa)) return false;
    mes=mm;anyo=aa;dia=dd;return true;
}

bool Fecha::incrementaAnyos(int inc){
    int yy=anyo+inc;
    if(!esFechaCorrecta(dia,mes,yy)) return false;
    anyo=yy;return true;
}

string Fecha::aCadena(bool larga, bool conDia) const {
    if(larga){
        // formato largo conDia = true: "lunes 9 de septiembre de 2024"
        // conDia = false: "9 de septiembre de 2024"
        if(conDia){
            return nombreDia(obtenerDiaSemana())+" "+to_string(dia)+" de "+nombreMes(mes)+" de "+to_string(anyo);
        } else {
            return to_string(dia)+" de "+nombreMes(mes)+" de "+to_string(anyo);
        }
    } else {
        // formato corto conDia = true: "lunes 9/9/2024"
        // conDia = false: "9/9/2024"
        if(conDia){
            return nombreDia(obtenerDiaSemana())+" "+to_string(dia)+"/"+to_string(mes)+"/"+to_string(anyo);
        } else {
            return to_string(dia)+"/"+to_string(mes)+"/"+to_string(anyo);
        }
    }
}


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
