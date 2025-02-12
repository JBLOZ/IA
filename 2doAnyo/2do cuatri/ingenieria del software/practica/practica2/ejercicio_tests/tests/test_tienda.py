import unittest
from src.tienda import calcular_total

class TestTienda(unittest.TestCase):
    def test_total_calculation(self):
        # Verifica que se calcule el total sin descuento
        carrito = [
            {'nombre': 'camiseta', 'precio': 15, 'cantidad': 2},
            {'nombre': 'pantalón', 'precio': 30, 'cantidad': 1}
        ]
        self.assertEqual(calcular_total(carrito), 60.0)

    def test_discount_application(self):
        # Verifica que se aplique correctamente el descuento
        carrito = [
            {'nombre': 'camiseta', 'precio': 15, 'cantidad': 2},
            {'nombre': 'pantalón', 'precio': 30, 'cantidad': 1}
        ]
        self.assertEqual(calcular_total(carrito, descuento=10), 54.0)
    
    def test_empty_cart(self):
        # Verifica el manejo de un carrito vacío
        self.assertEqual(calcular_total([], descuento=10), 0)

if __name__ == '__main__':
    unittest.main()