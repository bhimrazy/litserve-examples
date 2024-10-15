import tempfile
import litserve as ls
import whisper


class WhisperAPI(ls.LitAPI):
    def setup(self, device):
        self.model = whisper.load_model("tiny", device=device)

    def decode_request(self, request):
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file.write(request["audio"].file.read())
            audio_data = whisper.audio.load_audio(temp_file.name)
        return audio_data

    def predict(self, audio_data):
        return self.model.transcribe(audio_data, language="en")

    def encode_response(self, output):
        return {"text": output["text"]}


if __name__ == "__main__":
    api = WhisperAPI()
    server = ls.LitServer(api, api_path="/transcribe", timeout=60)
    server.run(port=8000)
