# Base Image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt first (for Docker layer caching)
COPY server/requirements.txt /app/requirements.txt

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the server source code
COPY server /app/server

# Also copy the generated folder and image_fetcher
COPY generated /app/generated
COPY image_fetcher.py /app/image_fetcher.py

# Set the PYTHONPATH to include the project root
ENV PYTHONPATH=/app

# Expose the gRPC port
EXPOSE 50051

# Run the server as a module
CMD ["python", "-m", "server.server"]
