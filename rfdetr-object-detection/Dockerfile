ARG PYTHON_VERSION=3.12
FROM python:$PYTHON_VERSION-slim

# Install system dependencies for OpenCV and other packages
RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgtk2.0-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# Install pytorch CPU version first (smaller footprint)
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install other requirements
RUN pip install --no-cache-dir litserve==0.2.7 -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "/app/server.py"]
