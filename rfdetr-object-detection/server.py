"""
Object detection API server using RF-DETR model.
Provides HTTP endpoints for detecting objects in uploaded images.
"""

import supervision as sv
from fastapi import UploadFile
from litserve import LitAPI, LitServer
from PIL import Image
from rfdetr import RFDETRBase
from rfdetr.util.coco_classes import COCO_CLASSES


class ObjectDetectionAPI(LitAPI):
    """API for object detection using RF-DETR model."""

    def setup(self, device):
        # Load the model
        self.model = RFDETRBase()
        self.model.model.model.to(device)
        self.coco_classes = COCO_CLASSES

    def decode_request(self, request: UploadFile) -> Image:
        with Image.open(request.file) as img:
            image = img.convert("RGB")
        return image

    def predict(self, image) -> sv.Detections:
        return self.model.predict(image)

    def encode_response(self, detections: sv.Detections):
        return {
            "detections": [
                {
                    "class_id": int(class_id),
                    "class_name": self.coco_classes[int(class_id)],
                    "confidence": float(confidence),
                    "bbox": bbox.tolist(),
                }
                for class_id, confidence, bbox in zip(
                    detections.class_id,
                    detections.confidence,
                    detections.xyxy,
                )
            ]
        }


if __name__ == "__main__":
    server = LitServer(ObjectDetectionAPI(), track_requests=True)
    server.run(port=8000)
