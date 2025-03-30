<h1 align="center">RF-DETR Object Detection API</h1>
<div align="center">
  <a target="_blank" href="https://lightning.ai/bhimrajyadav/studios/deploy-rf-detr-a-sota-real-time-object-detection-model-using-litserve">
  <img src="https://pl-bolts-doc-images.s3.us-east-2.amazonaws.com/app-2/studio-badge.svg" alt="Open In Studio"/>
</a>
</div>

## 🎯 Overview

The **RF-DETR Object Detection API** leverages the cutting-edge **RF-DETR** model to provide state-of-the-art object detection capabilities. RF-DETR is a real-time, transformer-based next-generation object detection model that combines the power of transformers with robust feature detection, enabling accurate and efficient object detection across a wide range of scenarios.

![RF-DETR Object Detection](https://github.com/user-attachments/assets/9079e257-a48c-46c1-883e-49516624982e)

### 🔑 Key Features
- **Transformer-Based Architecture**: RF-DETR uses a transformer backbone for robust feature extraction and detection.
- **End-to-End Object Detection**: No need for region proposals or anchor boxes.
- **High Accuracy**: Achieves state-of-the-art performance on COCO and other benchmarks.
- **Versatile Applications**: Ideal for real-time object detection in images and videos.

---

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.8+
- `pip` (Python package installer)

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/bhimrazy/litserve-examples.git
    cd litserve-examples/rfdetr-object-detection
    ```

2. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🖥️ Running the Server

Start the API server powered by [LitServe](https://github.com/Lightning-AI/LitServe):
```bash
python server.py
```

The server will start on `http://localhost:8000/predict`.

---

## 📤 Making a Request

To detect objects in an image, send a POST request to the `/predict` endpoint with the image file. Here's an example using `curl`:

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "request=@sample.jpeg"
```

Or use the provided Python client:
```bash
python client.py --image path/to/your/image.jpg

# example
python client.py --image sample.jpeg
```

---

## 📦 Example Response

```json
{
    "detections": [
        {
            "class_id": 1,
            "class_name": "person",
            "confidence": 0.98,
            "bbox": [50, 100, 200, 400]
        },
        {
            "class_id": 3,
            "class_name": "car",
            "confidence": 0.92,
            "bbox": [300, 150, 500, 300]
        }
    ]
}
```

---

## 📚 Documentation

### Model Features
- **Transformer Backbone**: RF-DETR uses a transformer-based architecture for feature extraction and detection.
- **COCO Classes**: Supports detection of 80 object categories from the COCO dataset.
- **Real-Time Performance**: Optimized for fast inference on modern GPUs.

### Resources
- [RF-DETR Blog](https://blog.roboflow.com/rf-detr/)
- [RF-DETR GitHub](https://github.com/roboflow/rf-detr)
- [LitServe Documentation](https://github.com/Lightning-AI/LitServe)
- [COCO Dataset Classes](https://cocodataset.org/#home)

---

## 🤝 Contributing

We welcome contributions from the community! If you'd like to contribute to this project, please read our [Contributing Guidelines](../CONTRIBUTING.md) to get started.

---

## 📜 License

This project is licensed under the [Apache License](../LICENSE).

---

Happy coding! 🎉
