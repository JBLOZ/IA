# Variables
CXX = g++
CXXFLAGS = -std=c++11 -Wall

# Archivos de objeto
OBJ = Fecha.o FechaUtils.o Ejemplo.o

# Archivo ejecutable
TARGET = Ejemplo

# Regla principal
$(TARGET): $(OBJ)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJ)

# Reglas para compilar los archivos de objeto
Ejemplo.o: Ejemplo.cc Fecha.h FechaUtils.h
	$(CXX) $(CXXFLAGS) -c Ejemplo.cc

Fecha.o: Fecha.cc Fecha.h FechaUtils.h
	$(CXX) $(CXXFLAGS) -c Fecha.cc

FechaUtils.o: FechaUtils.cc FechaUtils.h
	$(CXX) $(CXXFLAGS) -c FechaUtils.cc

# Limpiar archivos objeto y ejecutables
clean:
	rm -f $(OBJ) $(TARGET)
