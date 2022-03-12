import unittest
import aplicacion

class Test_aplicacion(unittest.TestCase):

    def test_start(self):
        self.assertTrue(aplicacion.App.cargaAcademica)

if __name__ == '__main__':
    unittest.main()