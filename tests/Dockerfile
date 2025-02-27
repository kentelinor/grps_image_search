# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY tests/requirements.txt /app/requirements.txt

# Install the dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the tests folder into the container
COPY tests /app/tests
COPY generated /app/generated  

# Set the environment variable for the Python path (if needed)
ENV PYTHONPATH=/app:/app/generated:/app/tests

# Run the tests (you can change to pytest or unittest as needed)
CMD ["python", "-m", "unittest", "discover", "-s", "tests"]
