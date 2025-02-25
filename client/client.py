import grpc
import os
import logging
import io
import time
from PIL import Image
from generated import image_search_pb2, image_search_pb2_grpc

def run():
    """
    Connects to the gRPC server, prompts the user for an image description,
    sends a SearchImage request, and displays the received image.
    """
    # Configure logging.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    
    # Use Docker service name to connect to the gRPC server
    # Default to "server" because that's the service name in docker-compose.yml
    host = os.getenv("GRPC_HOST", "server")
    port = os.getenv("GRPC_PORT", "50051")
    server_address = f"{host}:{port}"

    # Retry logic for gRPC connection
    max_retries = 10
    retry_delay = 5
    for attempt in range(max_retries):
        try:
            # Create a gRPC channel and stub.
            channel = grpc.insecure_channel(server_address)
            grpc.channel_ready_future(channel).result(timeout=10)
            stub = image_search_pb2_grpc.ImageSearchStub(channel)
            logging.info(f"Connected to gRPC server at {server_address}")
            break  # Exit the loop if connection is successful
        except grpc.RpcError as rpc_error:
            logging.error(f"Connection failed: {rpc_error}")
            logging.info(f"Retrying in {retry_delay} seconds... ({attempt + 1}/{max_retries})")
            time.sleep(retry_delay)
    else:
        logging.error("Failed to connect to gRPC server after multiple attempts.")
        return

    # Prompt the user for an image description.
    query = input("Enter image description: ").strip()
    if not query:
        logging.error("No description provided. Exiting.")
        return
    
    # Create the gRPC request.
    request = image_search_pb2.ImageRequest(description=query)
    
    try:
        # Call the SearchImage RPC.
        response = stub.SearchImage(request)
        
        if response.image_data:
            filename = "received_image.jpg"
            with open(filename, "wb") as f:
                f.write(response.image_data)
            logging.info(f"Image received and saved as '{filename}'.")
            
            # Attempt to display the image using Pillow.
            try:
                image = Image.open(io.BytesIO(response.image_data))
                image.show()
            except Exception as e:
                logging.error(f"Error displaying the image: {e}")
        else:
            logging.warning("No image data received.")
    
    except grpc.RpcError as rpc_error:
        logging.error(f"gRPC error: {rpc_error}")

if __name__ == "__main__":
    run()
