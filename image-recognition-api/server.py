import torch
from fastapi import UploadFile
from litserve import LitAPI, LitServer
from PIL import Image
from torchvision.models import ResNet50_Weights, resnet50


class ImageRecognitionAPI(LitAPI):
    def setup(self, device):
        self.device = device
        self.weights = ResNet50_Weights.IMAGENET1K_V2
        self.preprocess = self.weights.transforms()
        self.categories = self.weights.meta["categories"]
        self.model = resnet50(weights=self.weights)
        self.model.to(self.device)
        self.model.eval()

    def decode_request(self, request: UploadFile):
        with Image.open(request.file) as img:
            image = img.convert("RGB")
        batch = self.preprocess(image).unsqueeze(0).to(self.device)
        return batch

    def predict(self, batch):
        with torch.no_grad():
            prediction = self.model(batch).squeeze(0).softmax(0)
        return prediction

    def encode_response(self, prediction):
        class_idx = prediction.argmax().item()
        class_name = self.categories[class_idx]
        confidence = round(prediction[class_idx].item(), 5)
        return {"class": class_name, "confidence": confidence}


if __name__ == "__main__":
    api = ImageRecognitionAPI()
    server = LitServer(api)
    server.run(port=8000)
