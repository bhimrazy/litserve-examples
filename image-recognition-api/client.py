import argparse
import os
import requests
import logging


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Client to test the ImageRecognition API server."
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
