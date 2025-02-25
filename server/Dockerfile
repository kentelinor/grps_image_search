# Base Image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy everything from the project root (including image_fetcher.py)
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir grpcio grpcio-tools pillow requests

# Set the PYTHONPATH to include the project root
ENV PYTHONPATH=/app

# Expose the gRPC port
EXPOSE 50051

# Run the server as a module
CMD ["python", "-m", "server.server"]
