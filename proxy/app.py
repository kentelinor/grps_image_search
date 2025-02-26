from flask import Flask, request, jsonify
from flask_cors import CORS
import grpc
from generated.image_search_pb2 import ImageRequest, ImageResponse  # Correct imports for request and response types
from generated.image_search_pb2_grpc import ImageSearchStub  # Correct import for the ImageSearchStub


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/search', methods=['GET'])
def search_image():
    description = request.args.get('description')
    if not description:
        return jsonify({'error': 'Description is required'}), 400

    # gRPC connection to the server
    channel = grpc.insecure_channel('server:50051')
    stub = ImageSearchStub(channel)
    grpc_request = ImageRequest(description=description)

    try:
        grpc_response = stub.SearchImage(grpc_request)
        if grpc_response.image_data:
            # Convert binary image data to base64
            import base64
            image_base64 = base64.b64encode(grpc_response.image_data).decode('utf-8')
            return jsonify({'image': image_base64}), 200
        else:
            return jsonify({'error': 'No image found'}), 404
    except grpc.RpcError as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
