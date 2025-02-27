# client.py
import grpc
from generated.image_search_pb2 import ImageRequest
from generated.image_search_pb2_grpc import ImageSearchStub


class ImageSearchClient:
    def __init__(self, channel):
        self.stub = ImageSearchStub(channel)

    def search_image(self, description):
        request = ImageRequest(description=description)
        response = self.stub.SearchImage(request)
        return response.image_data, response.image_url
