#include <iostream>
#include <string>
#include <vector>
#include "Calendario.h"

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
