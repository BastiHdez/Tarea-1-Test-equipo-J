import unittest
import grpc
import distance_unary_pb2_grpc as pb2_grpc
import distance_unary_pb2 as pb2

class TestDistanceService(unittest.TestCase):
    def setUp(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = pb2_grpc.DistanceServiceStub(self.channel)

    def test_valid_distance_km(self):
        message = pb2.SourceDest(
            source=pb2.Position(latitude=-33.047255, longitude=-71.606330),
            destination=pb2.Position(latitude=-33.047317, longitude=-71.614301),
            unit="km"
        )
        response = self.stub.geodesic_distance(message)
        self.assertGreater(response.distance, 0)
        self.assertEqual(response.unit, "km")
        self.assertEqual(response.method, "geodesic")

    def tearDown(self):
        self.channel.close()

if __name__ == "__main__":
    unittest.main()
