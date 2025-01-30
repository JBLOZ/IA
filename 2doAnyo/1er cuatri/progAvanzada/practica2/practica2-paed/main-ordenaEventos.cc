#include<iostream>
#include<string>
using namespace std;

int main(){

  Calendario c;
  
  int d,m,a;
  string desc, sep;
  char car;
  
  cin >> d;
  while( d > 0){
    cin >> m;
    cin >> a;
    Fecha f(d,m,a);
    cin >> sep;
    
    cin.get(car);
    
    getline(cin,desc);
    
    c.insertarEvento(f,desc);
   
    cin >> d;
  }
  
  cout << c.aCadena()<< endl;

  return 0;

}
