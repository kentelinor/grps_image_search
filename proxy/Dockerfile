# Base Image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy proxy code and generated gRPC files
COPY proxy /app/proxy
COPY generated /app/generated

# Install dependencies including Flask-CORS
RUN pip install --no-cache-dir grpcio grpcio-tools Flask Flask-CORS

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Expose the Flask port
EXPOSE 8080

# Run Flask server
CMD ["python", "-m", "proxy.app"]
