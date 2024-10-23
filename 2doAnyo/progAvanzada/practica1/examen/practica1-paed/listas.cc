
#include <iostream>
#include <list>
#include <vector>
#include <deque>
using namespace std;


int main() {
    // 1. Trabajando con std::list
    std::list<int> miLista;

    // a. push_back: Agrega al final
    miLista.push_back(10);
    miLista.push_back(20);
    miLista.push_back(30);

    // b. push_front: Agrega al inicio
    miLista.push_front(5);

    // c. insert: Inserta en una posición específica
    auto it = miLista.begin();
    std::advance(it, 2); // Mover el iterador a la tercera posición
    miLista.insert(it, 15); // Insertar 15 antes de 20

    // d. emplace_back: Construye y agrega al final
    miLista.emplace_back(40);

    // e. emplace_front: Construye y agrega al inicio
    miLista.emplace_front(2);

    // f. splice: Mueve elementos de otra lista
    list<int> otraLista = {50, 60};
    miLista.splice(miLista.end(), otraLista); // Mueve todos los elementos de otraLista al final de miLista

    // Mostrar elementos de miLista
    cout << "Contenido de miLista (std::list): ";
    for(auto num:miLista) {
        std::cout << num << " ";
    }
    std::cout << "\n";

    // 2. Trabajando con std::vector
    vector<int> miVector;

    // a. push_back: Agrega al final
    miVector.push_back(100);
    miVector.push_back(200);
    miVector.push_back(300);

    // b. emplace_back: Construye y agrega al final
    miVector.emplace_back(400);

    // c. Acceso y modificación con []
    if(!miVector.empty()) {
        miVector[1] = 250; // Cambiar el segundo elemento de 200 a 250
    }

    // Mostrar elementos de miVector
    std::cout << "Contenido de miVector (std::vector): ";
    for(auto num : miVector) {
        std::cout << num << " ";
    }
    cout << "\n";

    // 3. Trabajando con std::deque
    deque<int> miDeque;

    // a. push_back: Agrega al final
    miDeque.push_back(1000);
    miDeque.push_back(2000);

    // b. push_front: Agrega al inicio
    miDeque.push_front(500);

    // c. emplace_back: Construye y agrega al final
    miDeque.emplace_back(3000);

    // d. emplace_front: Construye y agrega al inicio
    miDeque.emplace_front(100);

    // Mostrar elementos de miDeque
    cout << "Contenido de miDeque (std::deque): ";
    int tamañoD = miDeque.size();
    for(int i = 0; i < tamañoD; ++i) {
        std::cout << miDeque[i] << " ";
    }
    cout << "\n";

    // 4. Trabajando con arreglos (arrays)
    const int tamaño = 5;
    int miArray[tamaño] = {1, 2, 3, 4, 5};

    // a. Acceso y modificación con []
    miArray[2] = 30; // Cambiar el tercer elemento de 3 a 30

    // Mostrar elementos de miArray
    cout << "Contenido de miArray (array): ";
    for(int i = 0; i < tamaño; ++i) {
        cout << miArray[i] << " ";
    }
    cout << "\n";

    return 0;
}
