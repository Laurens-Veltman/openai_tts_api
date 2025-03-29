# OpenAI TTS API

This project provides a FastAPI-based web service for generating text-to-speech (TTS) audio using the demo service on 
openai.fm. The API converts input text into speech, which is downloaded as a MP3 file.

## Features:
- Text-to-Speech Generation: Converts text into speech.
- Customizable Parameters: Allows customization of voice options similar as on the website.
- API Endpoint: Exposes an endpoint (/generate_tts/) for easy access to TTS functionality.

1. Clone the repository:
```bash
git clone https://github.com/Laurens-Veltman/openai_tts_api
cd openai_tts_api
```
2. Run the container:
```bash
docker compose up -d --build
```
3. Access the server on port 8000. (e.g., localhost:8000/docs#/)
4. Write a prompt, play around with the voice settings.
5. Enjoy the result. Generated audio is stored in the project directory by default.

Please be mindful of the number of requests you make to the service. Abuse of the service or excessive 
requests may lead to rate limiting. It's recommended to use the service responsibly and to adhere to the OpenAI usage 
policies and guidelines. Please note that this API may stop working at any time if 
OpenAI decides to discontinue this demo service.

## License
This project is released under the MIT License.
## Acknowledgments
OpenAI -> [openai.fm](https://www.openai.fm/) for providing the awesome demo service.

This project is not affiliated with or endorsed by OpenAI
