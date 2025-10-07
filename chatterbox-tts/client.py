import argparse
import base64
import subprocess
import sys
from pathlib import Path

import requests

API_URL = "http://127.0.0.1:8000/speech"


def play_audio(file_path):
    """Play audio file using system default player."""
    try:
        # Try different audio players based on OS
        if sys.platform == "darwin":  # macOS
            subprocess.run(["afplay", file_path], check=True)
        elif sys.platform == "linux":
            subprocess.run(["aplay", file_path], check=True)
        elif sys.platform == "win32":
            subprocess.run(["cmd", "/c", "start", file_path], shell=True, check=True)
        else:
            print(f"⚠️ Auto-play not supported on {sys.platform}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to play audio file: {file_path}")
    except FileNotFoundError:
        print(
            f"❌ Audio player not found. Please install audio player or play {file_path} manually"
        )


def main():
    parser = argparse.ArgumentParser(description="Chatterbox TTS Client")
    parser.add_argument("--text", help="Text to synthesize")
    parser.add_argument(
        "--audio-prompt", help="Audio prompt file path for voice cloning (optional)"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="output.wav",
        help="Output audio file path (default: output.wav)",
    )
    parser.add_argument(
        "--play", action="store_true", help="Play the generated audio after synthesis"
    )
    parser.add_argument(
        "--exaggeration",
        type=float,
        default=0.5,
        help="Exaggeration level (0.0-1.0, default: 0.5)",
    )
    parser.add_argument(
        "--cfg", type=float, default=0.5, help="CFG weight (0.0-1.0, default: 0.5)"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.8,
        help="Temperature (0.0-1.0, default: 0.8)",
    )

    args = parser.parse_args()

    # Prepare request data
    data = {
        "text": args.text,
        "exaggeration": args.exaggeration,
        "cfg": args.cfg,
        "temperature": args.temperature,
    }

    # Add audio prompt if provided
    if args.audio_prompt:
        if not Path(args.audio_prompt).exists():
            print(f"❌ Audio prompt file not found: {args.audio_prompt}")
            sys.exit(1)
        with open(args.audio_prompt, "rb") as f:
            audio_data = f.read()
        audio_base64 = base64.b64encode(audio_data).decode("utf-8")
        data["audio_prompt"] = audio_base64
        print(f"🔊 Using voice from: {args.audio_prompt}")

    # Make API request
    try:
        response = requests.post(API_URL, json=data)
        response.raise_for_status()

        # Save audio to file
        with open(args.output, "wb") as f:
            f.write(response.content)

        print(f"✅ Audio saved to: {args.output}")

        # Play audio if requested
        if args.play:
            print("🔊 Playing audio...")
            play_audio(args.output)

    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response: {e.response.text}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
