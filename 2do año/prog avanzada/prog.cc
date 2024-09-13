#include <iostream>
using namespace std;
#include <cstdlib>
#include <ctime>
int main(){

    int a, b, c;
    a = 10;

    cout << a << endl;
    srand(static_cast<unsigned  int>(time(0)));
    a = rand() % 10;
    cout << a << endl;
    return 0;
}