import argparse
import requests


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Client to test the WhisperAPI server."
    )
    parser.add_argument(
        "-a",
        "--audio_file",  # Added short and long names for the argument
        type=str,
        required=True,
        help="Path to the audio file to be transcribed",
    )
    args = parser.parse_args()

    # API endpoint URL
    url = "http://localhost:8000/transcribe"

    # Open the audio file and send it to the server
    with open(args.audio_file, "rb") as audio:
        files = {"audio": audio}
        response = requests.post(url, files=files)

    # Print the server's response
    if response.status_code == 200:
        print("Transcription result:", response.json()["text"])
    else:
        print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    main()
