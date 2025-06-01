# Deployment Guide for Chatterbox TTS API

This guide covers different deployment options for the Chatterbox TTS API powered by LitServe.

## Local Development

### Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   python server.py
   ```

3. **Test the API:**
   ```bash
   python client.py
   ```

### Using the Startup Script

```bash
chmod +x start.sh
./start.sh
```

## Docker Deployment

### CPU-Only Deployment

```bash
# Build the image
docker build -t chatterbox-tts .

# Run the container
docker run -p 8000:8000 chatterbox-tts
```

### GPU-Enabled Deployment

```bash
# Build production image with CUDA support
docker build -f Dockerfile.prod -t chatterbox-tts-gpu .

# Run with GPU support
docker run --gpus all -p 8000:8000 chatterbox-tts-gpu
```

## Cloud Deployment

### AWS EC2

1. **Launch an EC2 instance** (recommended: g4dn.xlarge for GPU or t3.large for CPU)

2. **Install Docker:**
   ```bash
   sudo yum update -y
   sudo yum install -y docker
   sudo service docker start
   sudo usermod -a -G docker ec2-user
   ```

3. **Deploy the application:**
   ```bash
   git clone <your-repo>
   cd chatterbox-tts
   docker build -t chatterbox-tts .
   docker run -d -p 8000:8000 --restart unless-stopped chatterbox-tts
   ```

4. **Configure security group** to allow inbound traffic on port 8000

### Google Cloud Platform

1. **Create a Compute Engine instance** with GPU (optional)

2. **Install Docker and NVIDIA drivers** (for GPU instances):
   ```bash
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   
   # Install NVIDIA Docker runtime (GPU instances only)
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
   curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
   curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
   sudo apt-get update && sudo apt-get install -y nvidia-docker2
   sudo systemctl restart docker
   ```

3. **Deploy the application:**
   ```bash
   git clone <your-repo>
   cd chatterbox-tts
   docker build -f Dockerfile.prod -t chatterbox-tts-gpu .
   docker run -d -p 8000:8000 --gpus all --restart unless-stopped chatterbox-tts-gpu
   ```

### Azure Container Instances

1. **Create a resource group:**
   ```bash
   az group create --name chatterbox-rg --location eastus
   ```

2. **Deploy container:**
   ```bash
   az container create \
     --resource-group chatterbox-rg \
     --name chatterbox-tts \
     --image <your-registry>/chatterbox-tts:latest \
     --cpu 2 \
     --memory 4 \
     --ports 8000 \
     --dns-name-label chatterbox-tts-api
   ```

## Kubernetes Deployment

### Create Kubernetes manifests:

**deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chatterbox-tts
spec:
  replicas: 2
  selector:
    matchLabels:
      app: chatterbox-tts
  template:
    metadata:
      labels:
        app: chatterbox-tts
    spec:
      containers:
      - name: chatterbox-tts
        image: chatterbox-tts:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        env:
        - name: CUDA_VISIBLE_DEVICES
          value: ""
---
apiVersion: v1
kind: Service
metadata:
  name: chatterbox-tts-service
spec:
  selector:
    app: chatterbox-tts
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

**Deploy:**
```bash
kubectl apply -f deployment.yaml
```

## Performance Optimization

### CPU Optimization

- Use `torch.set_num_threads()` to control CPU thread usage
- Consider using Intel MKL or OpenBLAS for better CPU performance
- Use quantized models if available

### GPU Optimization

- Use mixed precision (float16) for faster inference
- Batch multiple requests when possible
- Monitor GPU memory usage and adjust batch sizes accordingly

### Memory Optimization

- Use model sharding for very large models
- Implement model caching strategies
- Monitor and limit concurrent requests

## Monitoring and Logging

### Health Checks

The API includes a health endpoint at `/health`:

```bash
curl http://localhost:8000/health
```

### Logging

Configure logging in `config.py`:

```python
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "/var/log/chatterbox-tts.log"  # Log to file
}
```

### Metrics Collection

Consider integrating with:
- Prometheus for metrics collection
- Grafana for visualization
- ELK Stack for log analysis

## Security Considerations

### API Security

1. **Enable API key authentication:**
   ```python
   SECURITY_CONFIG = {
       "require_api_key": True,
       "api_key": "your-secure-api-key"
   }
   ```

2. **Rate limiting:**
   ```python
   SECURITY_CONFIG = {
       "max_requests_per_minute": 60
   }
   ```

3. **CORS configuration:**
   ```python
   SECURITY_CONFIG = {
       "enable_cors": True,
       "allowed_origins": ["https://yourdomain.com"]
   }
   ```

### Network Security

- Use HTTPS in production
- Configure firewall rules to restrict access
- Use VPN or private networks when possible

## Scaling Strategies

### Horizontal Scaling

- Deploy multiple instances behind a load balancer
- Use container orchestration (Kubernetes, Docker Swarm)
- Implement request queuing for high loads

### Vertical Scaling

- Increase CPU/memory resources
- Use GPU instances for better performance
- Optimize model loading and caching

## Troubleshooting

### Common Issues

1. **Model loading errors:**
   - Check available memory
   - Verify CUDA installation (for GPU)
   - Check network connectivity for model downloads

2. **Audio generation failures:**
   - Validate input text length
   - Check audio format compatibility
   - Monitor system resources

3. **Performance issues:**
   - Monitor CPU/GPU utilization
   - Check memory usage
   - Optimize batch sizes

### Debug Mode

Enable debug logging:
```python
LOGGING_CONFIG = {
    "level": "DEBUG"
}
```

### Testing

Run the comprehensive test suite:
```bash
python test_suite.py
```

## Production Checklist

- [ ] Configure proper logging
- [ ] Set up monitoring and alerting
- [ ] Enable security features (API keys, rate limiting)
- [ ] Configure HTTPS
- [ ] Set up backup and recovery procedures
- [ ] Test failover scenarios
- [ ] Document API usage and limits
- [ ] Set up CI/CD pipelines
