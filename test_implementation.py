import unittest
import grpc
import distance_unary_pb2_grpc as pb2_grpc
import distance_unary_pb2 as pb2


class TestDistanceService(unittest.TestCase):
    def setUp(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = pb2_grpc.DistanceServiceStub(self.channel)

    def test_valid_distance_km(self):
        # Latitud válida, Longitud válida
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-33.0351516, longitude=-70.5955963),
            destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
            unit="km"
        )
        response = self.stub.geodesic_distance(message)
        self.assertGreater(response.distance, 0)  # Se espera una distancia positiva
        self.assertEqual(response.unit, "km")  # Se espera que la unidad sea km
        self.assertEqual(response.method, "geodesic")  # Se espera que el método sea geodésico

    def test_latitude_out_of_range(self):
        # Latitud fuera de rango, Longitud válida
        message = pb2.SourceDest(
            source=pb2.Position(latitude=91.0, longitude=-70.5955963),  # Latitud inválida
            destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
            unit="km"
        )
        response = self.stub.geodesic_distance(message)
        self.assertEqual(response.distance, -1)  # Se espera que la distancia sea -1
        self.assertEqual(response.unit, "invalid")  # Se espera unidad inválida

    def test_longitude_out_of_range(self):
        # Latitud válida, Longitud fuera de rango
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-33.0351516, longitude=181.0),  # Longitud inválida
            destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
            unit="km"
        )
        response = self.stub.geodesic_distance(message)
        self.assertEqual(response.distance, -1)  # Se espera que la distancia sea -1
        self.assertEqual(response.unit, "invalid")  # Se espera unidad inválida

    def test_latitude_longitude_out_of_range(self):
        # Latitud y Longitud fuera de rango
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-91.0, longitude=181.0),  # Ambos inválidos
            destination=pb2.Position(latitude=0.0, longitude=0.0),
            unit="km"
        )
        response = self.stub.geodesic_distance(message)
        self.assertEqual(response.distance, -1)  # Se espera que la distancia sea -1
        self.assertEqual(response.unit, "invalid")  # Se espera unidad inválida

    def test_unit_valid_km(self):
        # Unidad válida "km"
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-33.0351516, longitude=-70.5955963),
            destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
            unit="km"
        )
        response = self.stub.geodesic_distance(message)
        self.assertGreater(response.distance, 0)  # Se espera una distancia válida

    def test_unit_valid_nm(self):
        # Unidad válida "nm"
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-33.0351516, longitude=-70.5955963),
            destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
            unit="nm"
        )
        response = self.stub.geodesic_distance(message)
        self.assertGreater(response.distance, 0)  # Se espera una distancia válida

    def test_unit_empty(self):
        # Unidad en blanco
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-33.0351516, longitude=-70.5955963),
            destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
            unit=""
        )
        response = self.stub.geodesic_distance(message)
        self.assertGreater(response.distance, 0)  # Se espera distancia válida en km por defecto

    def test_unit_invalid(self):
        # Unidad no válida
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-33.0351516, longitude=-70.5955963),
            destination=pb2.Position(latitude=-33.0348327, longitude=-71.5980458),
            unit="invalid"
        )
        with self.assertRaises(grpc.RpcError) as cm:  # Espera una excepción de tipo RpcError
            self.stub.geodesic_distance(message)

        self.assertEqual(cm.exception.code(), grpc.StatusCode.UNKNOWN)  # Verifica que el código de error sea UNKNOWN
        self.assertIn("Exception calling application", cm.exception.details())  # Verifica detalles del error

    def tearDown(self):
        self.channel.close()


if __name__ == "__main__":
    unittest.main()
