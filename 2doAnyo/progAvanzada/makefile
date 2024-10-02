CXX = g++

# Flags de compilación
CXXFLAGS = -std=c++11 -Wall -g

# Nombre del ejecutable
TARGET = Ejemplo

# Archivos fuente
SOURCES = Ejemplo.cc Fecha.cc FechaUtils.cc

# Archivos objeto generados a partir de los fuentes
OBJECTS = $(SOURCES:.cc=.o)

# Regla principal
all: $(TARGET)

# Compilación del ejecutable
$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $@ $^

# Regla genérica para compilar archivos .cc a .o
%.o: %.cc
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Dependencias
Ejemplo.o: Ejemplo.cc Fecha.h FechaUtils.h
Fecha.o: Fecha.cc Fecha.h FechaUtils.h
FechaUtils.o: FechaUtils.cc FechaUtils.h

# Limpiar archivos generados
clean:
	rm -f $(OBJECTS) $(TARGET)

# Regla para ejecutar el programa
run: $(TARGET)
	./$(TARGET)

.PHONY: all clean run