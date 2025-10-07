import argparse
import logging
import os

import numpy as np
import requests
import supervision as sv
from PIL import Image


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Client to test the Object Detection API server."
    )
    parser.add_argument(
        "-i",
        "--image",
        type=str,
        required=True,
        help="Path to the image file to send to the server.",
    )
    return parser.parse_args()


def check_image_file(image_path):
    if not os.path.isfile(image_path):
        logging.error(f"Image file '{image_path}' does not exist.")
        return False
    return True


def send_image_to_server(image_path, url):
    try:
        with open(image_path, "rb") as image_file:
            files = {"request": image_file}
            response = requests.post(url, files=files)

        if response.status_code == 200:
            logging.info("Result: %s", response.json())

            detections = response.json()["detections"]
            sv_detections = sv.Detections(
                class_id=np.array([detection["class_id"] for detection in detections]),
                confidence=np.array(
                    [detection["confidence"] for detection in detections]
                ),
                xyxy=np.array([detection["bbox"] for detection in detections]),
            )
            labels = [
                f"{detection['class_name']} {detection['confidence']:.2f}"
                for detection in detections
            ]

            annotated_image = Image.open(image_path)
            annotated_image = sv.BoxAnnotator().annotate(annotated_image, sv_detections)
            annotated_image = sv.LabelAnnotator().annotate(
                annotated_image, sv_detections, labels
            )

            # save the annotated image
            file_name = (
                f"{os.path.splitext(os.path.basename(image_path))[0]}_annotated.jpg"
            )
            file_path = os.path.join(os.path.dirname(image_path), file_name)
            annotated_image.save(file_path)
            logging.info("Annotated image saved to: %s", file_path)

        else:
            logging.error("Error: %s %s", response.status_code, response.text)
    except Exception as e:
        logging.error("An error occurred: %s", str(e))


def main():
    logging.basicConfig(level=logging.INFO)
    args = parse_arguments()

    if check_image_file(args.image):
        API_URL = "http://localhost:8000/predict"
        send_image_to_server(args.image, API_URL)


if __name__ == "__main__":
    main()
