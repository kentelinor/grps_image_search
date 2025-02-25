import grpc
import os
import sys
import logging
import signal
import time
from concurrent import futures

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# Ensure the project root is on the Python path.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Add the 'generated' folder to sys.path so that top-level imports work.
generated_path = os.path.join(project_root, 'generated')
sys.path.insert(0, generated_path)

# Import the generated gRPC modules and image fetching logic
from generated import image_search_pb2, image_search_pb2_grpc
from image_fetcher import fetch_image_url, download_image

class ImageSearchService(image_search_pb2_grpc.ImageSearchServicer):
    """
    Implements the ImageSearch gRPC service.
    Receives a query, retrieves an image URL using fetch_image_url,
    downloads the image using download_image, and returns the image data.
    """
    def SearchImage(self, request, context):
        logging.info(f"Received request: {request.description}")
        
        # Fetch image URL based on the description.
        image_url = fetch_image_url(request.description)
        if not image_url:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No image found for the given description.")
            return image_search_pb2.ImageResponse()

        # Download the image data.
        image_data = download_image(image_url)
        if not image_data:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to download the image.")
            return image_search_pb2.ImageResponse()
        
        # Return the image data in the response.
        return image_search_pb2.ImageResponse(image_data=image_data)

def serve():
    """
    Starts the gRPC server on a port specified by the GRPC_PORT environment variable,
    defaulting to 50051 if not set. Registers signal handlers for graceful shutdown.
    """
    # Use environment variable for port configuration.
    port = os.getenv("GRPC_PORT", "50051")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    image_search_pb2_grpc.add_ImageSearchServicer_to_server(ImageSearchService(), server)
    
    server_address = f"0.0.0.0:{port}"

    server.add_insecure_port(server_address)
    server.start()
    logging.info(f"Server is running on port {port}...")

    # Define a graceful shutdown handler.
    def shutdown_handler(signum, frame):
        logging.info("Shutdown signal received. Stopping server gracefully...")
        server.stop(0)
        sys.exit(0)

    # Register signal handlers for graceful shutdown.
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    # Keep the server running indefinitely.
    try:
        while True:
            time.sleep(86400)  # Sleep for one day.
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt received. Shutting down server...")
        server.stop(0)

if __name__ == "__main__":
    serve()
