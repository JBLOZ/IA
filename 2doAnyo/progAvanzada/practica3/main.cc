#include <iostream>
#include <string>
#include <vector>
#include "Calendario.h"

using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<string> categorias;
    {
        // Leer categorías hasta [FIN_CATEGORIAS]
        string line;
        while(true){
            if(!std::getline(cin,line)) break;
            if(line=="[FIN_CATEGORIAS]") break;
            categorias.push_back(line);
        }
    }

    Calendario cal;
    string comando;
    while(true){
        if(!(cin>>comando)) break;
        if(comando=="[FIN]") break;
        if(comando=="insertarEvento"){
            int d,m,a,cat;
            string t,desc;
            cin >> d >> m >> a >> t >> desc >> cat;
            // reemplazar '_' por ' ' en t y desc
            for(auto &c:t) if(c=='_') c=' ';
            for(auto &c:desc) if(c=='_') c=' ';
            Evento ev(Fecha(d,m,a),t,desc,cat);
            bool res = cal.insertarEvento(ev);
            cout<<(res?1:0)<<'\n';
        } else if(comando=="eliminarEvento"){
            int d,m,a;
            cin >> d >> m >> a;
            bool res = cal.eliminarEvento(Fecha(d,m,a));
            cout<<(res?1:0)<<'\n';
        } else if(comando=="comprobarEvento"){
            int d,m,a;
            cin >> d >> m >> a;
            bool res = cal.comprobarEvento(Fecha(d,m,a));
            cout<<(res?1:0)<<'\n';
        } else if(comando=="obtenerEvento"){
            int d,m,a;
            cin >> d >> m >> a;
            Evento ev = cal.obtenerEvento(Fecha(d,m,a));
            cout<<ev.aCadena(categorias)<<'\n';
        } else if(comando=="aCadena"){
            string s = cal.aCadena(categorias);
            if(!s.empty()) cout<<s<<'\n';
        } else if(comando=="aCadenaPorTitulo"){
            string t;
            cin >> t;
            for(auto &c:t) if(c=='_') c=' ';
            string s = cal.aCadenaPorTitulo(t,categorias);
            if(!s.empty()) cout<<s<<'\n';
        } else if(comando=="categoriaMasFrecuente"){
            cout<<cal.categoriaMasFrecuente()<<'\n';
        } else if(comando=="diaMasFrecuente"){
            cout<<cal.diaMasFrecuente()<<'\n';
        } else if(comando=="mesMasFrecuente"){
            cout<<cal.mesMasFrecuente()<<'\n';
        } else if(comando=="anyoMasFrecuente"){
            cout<<cal.anyoMasFrecuente()<<'\n';
        } else if(comando=="deshacerInsercion"){
            cal.deshacerInsercion();
            // void, no imprime nada
        } else if(comando=="deshacerBorrado"){
            cal.deshacerBorrado();
            // void, no imprime nada
        }
    }

    return 0;
}
