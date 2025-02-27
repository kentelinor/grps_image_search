import unittest
import grpc
from generated.image_search_pb2 import ImageRequest
from generated.image_search_pb2_grpc import ImageSearchStub


class TestImageSearchClient(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel = grpc.insecure_channel('server:50051')  # Assuming server is up and running at this address
        self.stub = ImageSearchStub(self.channel)

    def test_search_image(self):
        # Test code for the 'SearchImage' method
        request = ImageRequest(description="small white dog")
        response = self.stub.SearchImage(request)

        self.assertIsNotNone(response.image_data)
        self.assertIsInstance(response.image_data, bytes)
        self.assertIsNotNone(response.image_url)

    def tearDown(self):
        self.channel.close()


if __name__ == '__main__':
    unittest.main()
