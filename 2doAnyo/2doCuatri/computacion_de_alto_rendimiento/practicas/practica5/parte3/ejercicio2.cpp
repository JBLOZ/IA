#include <iostream>
#include <vector>
#include <string>
#include <cstdlib>
#include <ctime>
#include <omp.h>
#include <map>
#include <iomanip>

// Estructura para almacenar los datos de cada usuario
struct UserData {
    int id;
    std::string detectedLanguage;
    double latitude;
    double longitude;
    std::string region;
    bool languageAdaptation;
};

// Función que simula la detección de idioma a partir de una muestra de audio.
// Se selecciona aleatoriamente un idioma de una lista.
std::string simulateLanguageDetection(unsigned int* seed) {
    int idx = rand_r(seed) % 4;
    static const std::string languages[4] = {"English", "Spanish", "French", "Portuguese"};
    return languages[idx];
}

// Función que determina la región del usuario en función de sus coordenadas GPS.
std::string getRegion(double lat, double lon) {
    if (lat >= 0) {
        if (lon >= 0)
            return "Region A";  // Predominante: English
        else
            return "Region B";  // Predominante: French
    } else {
        if (lon >= 0)
            return "Region C";  // Predominante: Spanish
        else
            return "Region D";  // Predominante: Portuguese
    }
}

// Función que devuelve el idioma predominante según la región.
std::string getPredominantLanguage(const std::string& region) {
    if (region == "Region A") return "English";
    else if (region == "Region B") return "French";
    else if (region == "Region C") return "Spanish";
    else return "Portuguese";
}

int main() {
    // Número de usuarios a simular
    const int numUsers = 1000000;
    std::vector<UserData> users(numUsers);

    // Medición del tiempo de procesamiento
    double startTime = omp_get_wtime();

    // Procesamiento paralelo de cada usuario utilizando OpenMP
    #pragma omp parallel for schedule(dynamic)
    for (int i = 0; i < numUsers; i++) {
        // Cada hilo utiliza su propia semilla para la generación aleatoria
        unsigned int seed = i + omp_get_thread_num();  // Se puede agregar omp_get_thread_num() para mayor variabilidad

        // Simulación del reconocimiento de la huella de voz: asignación de un ID único
        users[i].id = i;

        // Simulación de la detección del idioma a partir de la muestra de audio
        users[i].detectedLanguage = simulateLanguageDetection(&seed);

        // Simulación de la obtención de coordenadas GPS (latitud y longitud aleatorias)
        double randLat = -90.0 + (rand_r(&seed) / (double)RAND_MAX) * 180.0;
        double randLon = -180.0 + (rand_r(&seed) / (double)RAND_MAX) * 360.0;
        users[i].latitude = randLat;
        users[i].longitude = randLon;

        // Determinar la región basada en las coordenadas GPS
        users[i].region = getRegion(randLat, randLon);

        // Obtener el idioma predominante para la región y comparar con el idioma detectado
        std::string predominantLanguage = getPredominantLanguage(users[i].region);
        users[i].languageAdaptation = (users[i].detectedLanguage != predominantLanguage);
    }

    double processingTime = omp_get_wtime() - startTime;

    // Análisis estadístico: conteo de usuarios por idioma
    std::map<std::string, int> languageCounts;
    #pragma omp parallel for schedule(dynamic)
    for (int i = 0; i < numUsers; i++) {
        // Se utiliza critical para evitar condiciones de carrera en el acceso al mapa
        #pragma omp critical
        {
            languageCounts[users[i].detectedLanguage]++;
        }
    }

    // Análisis estadístico: conteo de usuarios que requieren adaptación por región
    std::map<std::string, int> adaptationCounts;
    #pragma omp parallel for schedule(dynamic)
    for (int i = 0; i < numUsers; i++) {
        if (users[i].languageAdaptation) {
            #pragma omp critical
            {
                adaptationCounts[users[i].region]++;
            }
        }
    }

    // Conteo total de usuarios que requieren adaptación utilizando la directiva reduction
    int totalAdaptations = 0;
    #pragma omp parallel for reduction(+:totalAdaptations) schedule(dynamic)
    for (int i = 0; i < numUsers; i++) {
        if (users[i].languageAdaptation)
            totalAdaptations++;
    }

    // Impresión de resultados y estadísticas
    std::cout << "Tiempo de procesamiento: " << processingTime << " segundos.\n";
    std::cout << "\nDistribución de usuarios por idioma:\n";
    for (auto &entry : languageCounts) {
        std::cout << "  " << entry.first << ": " << entry.second << "\n";
    }

    std::cout << "\nUsuarios que requieren adaptación de idioma por región:\n";
    for (auto &entry : adaptationCounts) {
        std::cout << "  " << entry.first << ": " << entry.second << "\n";
    }
    std::cout << "\nTotal de usuarios que requieren adaptación: " << totalAdaptations << "\n";

    // Simulación de la generación de un mapa global: se muestran los datos de geolocalización de los primeros 5 usuarios
    std::cout << "\nMuestra de datos de geolocalización (ultimos 15 usuarios):\n";
    for (int i = numUsers - 1; i > numUsers - 16; i--) {
        std::cout << "Usuario " << users[i].id
                  << " - Latitud: " << std::fixed << std::setprecision(2) << users[i].latitude
                  << ", Longitud: " << users[i].longitude
                  << ", Región: " << users[i].region
                  << ", Idioma detectado: " << users[i].detectedLanguage
                  << ", Adaptación sugerida: " << (users[i].languageAdaptation ? "Sí" : "No")
                  << "\n";
    }

    return 0;
}
