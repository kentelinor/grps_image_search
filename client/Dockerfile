# Base Image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the client source code
COPY client /app/client

# Also copy the generated folder
COPY generated /app/generated

# Install dependencies
RUN pip install --no-cache-dir grpcio grpcio-tools pillow requests

# Set the PYTHONPATH to include the current working directory
ENV PYTHONPATH /app

# Expose the gRPC port (not strictly necessary for the client, but good practice)
EXPOSE 50051

# Run the client as a module
CMD ["python", "-m", "client.client"]
