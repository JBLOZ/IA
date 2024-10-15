
#include <iostream>
#include <string>
using namespace std;




int main() {

    int lista1[7] = {1, 2, 3, 4, 5, 6, 7};
    int *i;
    i = &lista1[7];

    cout << *i << endl;
    return 0;
}