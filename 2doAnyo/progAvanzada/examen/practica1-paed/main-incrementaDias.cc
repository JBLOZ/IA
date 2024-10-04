#include<iostream>
using namespace std;

int main(){
   int d,m,a, inc;
   
   cin >> d;
   cin >> m;
   cin >>a;
   cin >> inc;
   
   Fecha f(d,m,a);
   f.incrementaDias(inc);
   cout << f.aCadena(false,false) << endl;
   
   return 0;
}
