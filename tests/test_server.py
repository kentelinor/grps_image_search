import unittest
import grpc
from unittest.mock import patch
from generated.image_search_pb2 import ImageRequest, ImageResponse
from generated.image_search_pb2_grpc import ImageSearchStub

class TestImageSearchService(unittest.TestCase):

    @patch.object(ImageSearchStub, 'SearchImage', return_value=ImageResponse(image_data=b"fake_image_data", image_url="http://example.com/fake_image.jpg"))
    def test_search_image_success(self, mock_search_image):
        # Mocking the server response for a search request
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = ImageSearchStub(channel)
            request = ImageRequest(description="small white dog")
            response = stub.SearchImage(request)
            
            # Test if image_data and image_url are not None and correct type
            self.assertIsNotNone(response.image_data)
            self.assertIsInstance(response.image_data, bytes)
            self.assertIsNotNone(response.image_url)
            self.assertEqual(response.image_url, "http://example.com/fake_image.jpg")

    @patch.object(ImageSearchStub, 'SearchImage', return_value=ImageResponse(image_data=b"", image_url="No image found"))
    def test_search_image_no_result(self, mock_search_image):
        # Mocking a no result response
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = ImageSearchStub(channel)
            request = ImageRequest(description="nonexistent image")
            response = stub.SearchImage(request)
            
            # Test if image_data is empty and image_url is the error message
            self.assertEqual(response.image_data, b"")
            self.assertEqual(response.image_url, "No image found")

if __name__ == '__main__':
    unittest.main()
