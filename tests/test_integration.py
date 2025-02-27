import unittest
import grpc
from generated.image_search_pb2 import ImageRequest
from generated.image_search_pb2_grpc import ImageSearchStub


class TestImageSearchIntegration(unittest.TestCase):

    def test_search_image_integration(self):
        # Test code for the 'SearchImage' method using the real server
        with grpc.insecure_channel('server:50051') as channel:
            stub = ImageSearchStub(channel)
            request = ImageRequest(description="small white dog")
            response = stub.SearchImage(request)

            # Assert that the response contains valid data
            self.assertIsNotNone(response.image_data)
            self.assertIsInstance(response.image_data, bytes)
            self.assertIsNotNone(response.image_url)


if __name__ == '__main__':
    unittest.main()
