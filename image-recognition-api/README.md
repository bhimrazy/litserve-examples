<h1 align="center">ImageRecognition API with LitServe</h1>

Welcome to the **ImageRecognition API**! This API enables powerful and efficient image recognition capabilities, seamlessly deployed using LitServe. Whether you're building an app for e-commerce, healthcare, or any other domain, this API delivers fast, reliable, and easy-to-integrate solutions.

![ImageRecognition API](https://github.com/user-attachments/assets/a9a195b3-8fab-4e84-957e-9a522aa83ad4)

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.8+
- `pip` (Python package installer)

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/bhimrazy/litserve-examples.git
    cd image-recognition-api
    ```

2. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Server

Start the API server powered by [LitServe](https://github.com/Lightning-AI/LitServe):
```bash
python server.py
```

The server will start on `http://localhost:8000/predict`.

### Making a Request

To recognize an image, send a POST request to the `/predict` endpoint with the image file. Here's an example using `curl`:

```bash
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'request=@cat.jpg;type=image/jpeg'
```

Test using the provided Python client:
```bash
python client.py --image cat.jpg
```

### Example Response

```json
{
    "label": "cat",
    "confidence": 0.98
}
```

## 📚 Documentation

For more detailed information, refer to the following resources:
- [LitServe Documentation](https://github.com/Lightning-AI/LitServe)
- [Torchvision Models](https://pytorch.org/vision/stable/models.html)

## 🤝 Contributing

We welcome contributions from the community! If you'd like to contribute to this project, please read our [Contributing Guidelines](../CONTRIBUTING.md) to get started.

## 📜 License

This project is licensed under the [Apache License](../LICENSE).

---

Developed and maintained with ❤️ by [Bhimraj Yadav](https://github.com/bhimrazy).

Happy coding! 🎉