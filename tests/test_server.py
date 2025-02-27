import unittest
import grpc
from generated.image_search_pb2 import ImageRequest, ImageResponse
from generated.image_search_pb2_grpc import ImageSearchStub


class TestImageSearchService(unittest.TestCase):

    def test_search_image_success(self):
        # Test code for the 'SearchImage' method
        # Here you'd mock the service call or test with the real service
        with grpc.insecure_channel('server:50051') as channel:
            stub = ImageSearchStub(channel)
            request = ImageRequest(description="small white dog")
            response = stub.SearchImage(request)  # No need to assign manually

            self.assertIsNotNone(response.image_data)
            self.assertIsInstance(response.image_data, bytes)
            self.assertIsNotNone(response.image_url)


if __name__ == '__main__':
    unittest.main()
