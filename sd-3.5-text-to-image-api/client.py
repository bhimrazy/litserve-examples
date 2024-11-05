import requests
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Generate an image from a prompt using an API."
    )
    parser.add_argument(
        "-p", "--prompt", type=str, help="The prompt to send to the API."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="generated_image.png",
        help="The output file name for the generated image.",
    )
    args = parser.parse_args()

    response = requests.post(
        "http://127.0.0.1:8000/generate", json={"prompt": args.prompt}
    )

    if response.status_code == 200:
        with open(args.output, "wb") as file:
            file.write(response.content)
        print(f"Image successfully saved as {args.output}")
    else:
        print(
            f"Failed to generate image. Status: {response.status_code}\nResponse: {response.text}"
        )


if __name__ == "__main__":
    main()
