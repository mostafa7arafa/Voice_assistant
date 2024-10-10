---
# Voice Assistant with Screen Capture and Speech Recognition

This Python project implements a voice assistant that captures the desktop screen, listens for user prompts via speech, and responds with audio output. It leverages OpenAI’s API for speech-to-text (STT) and text-to-speech (TTS), and uses Google Generative AI (`gemini-1.5-flash-latest`) for natural language processing (NLP) to generate responses based on the user’s voice input and desktop content.

## Key Features
- **Desktop Screen Capture**: Continuously captures the desktop and uses it as context for responses.
- **Voice-Activated Commands**: Listens for user input through speech and converts it to text using OpenAI’s Whisper model.
- **AI-Powered Responses**: Generates concise and informative answers using Google Generative AI, considering the desktop’s contents.
- **Text-to-Speech (TTS)**: Converts the AI’s textual response back into speech and plays it through the system speakers.
- **Lightweight & Multithreaded**: Runs efficiently with multi-threading for capturing screenshots and processing voice input simultaneously.

---

## Table of Contents
1. [Project Architecture](#project-architecture)
2. [Components Overview](#components-overview)
3. [Installation](#installation)
4. [Environment Variables](#environment-variables)
5. [How to Run the Project](#how-to-run-the-project)
6. [How It Works](#how-it-works)
7. [Usage Example](#usage-example)
8. [Known Issues](#known-issues)
9. [Future Enhancements](#future-enhancements)
10. [License](#license)

---

## Project Architecture

The project consists of two main classes: 
1. **`DesktopScreenshot`**: Captures desktop screenshots at regular intervals, encodes them as JPEG images, and stores them in memory. This class runs on a separate thread to avoid blocking other operations.
2. **`Assistant`**: Manages the voice-to-text transcription, image processing, prompt generation, and text-to-speech (TTS) conversion. It uses OpenAI’s Whisper model for speech recognition and Google Generative AI for NLP.

The assistant operates in a feedback loop:
- **Input**: Takes screenshots of the desktop and listens for user voice commands.
- **Processing**: Sends the text prompt (user input) and a screenshot (desktop image) to the AI model to generate a response.
- **Output**: Converts the AI-generated response to speech and plays it.

---

## Components Overview

### 1. **DesktopScreenshot**
- **Function**: Captures periodic desktop screenshots.
- **Methods**:
    - `start()`: Starts the screenshot thread.
    - `read(encode=True)`: Returns the latest screenshot in base64-encoded format.
    - `stop()`: Stops the screenshot thread.

### 2. **Assistant**
- **Function**: Manages speech recognition, AI-powered question answering, and TTS.
- **Methods**:
    - `answer(prompt, image)`: Processes the user's prompt and desktop image to generate a response.
    - `_tts(response)`: Converts the AI-generated response to speech and plays it using the system speakers.
    - `_create_inference_chain()`: Builds the language model inference chain using LangChain.

---

## Installation

### 1. **Clone the Repository**
```bash
git clone https://github.com/your-username/voice-assistant.git
cd voice-assistant
```

### 2. **Install Dependencies**
Make sure you have Python 3.7+ installed. Then install the required dependencies using `pip`:
```bash
pip install -r requirements.txt
```

### 3. **Install Additional Dependencies (Optional)**
If you face issues with `pyaudio`, you may need to install it manually:
- On Windows:
    ```bash
    pip install pipwin
    pipwin install pyaudio
    ```
- On macOS/Linux:
    ```bash
    brew install portaudio
    pip install pyaudio
    ```

---

## Environment Variables

You need to create a `.env` file to securely store your API keys. The `.env` file should be placed in the root directory and contain the following keys:

```env
# .env file

OPENAI_API_KEY=your_openai_api_key
GOOGLE_GENAI_KEY=your_google_genai_key
```

You can obtain your API keys from:
- OpenAI: [OpenAI API](https://platform.openai.com/)
- Google Generative AI: [Google Cloud Console](https://console.cloud.google.com/)

---

## How to Run the Project

1. **Run the Script**:
   Once the dependencies are installed and the `.env` file is configured, you can run the project:

    ```bash
    python assistant.py
    ```

2. **Adjust for Ambient Noise**:
   The assistant will automatically adjust for ambient noise before starting to listen for commands.

---

## How It Works

- **Step 1**: The script continuously captures screenshots of the desktop and stores them.
- **Step 2**: The microphone listens for voice commands. When the user speaks, it uses OpenAI’s Whisper model to convert the audio input to text.
- **Step 3**: The transcribed text and the latest screenshot are sent to the assistant’s inference chain, which processes the prompt using Google Generative AI.
- **Step 4**: The AI generates a response, which is converted into speech using OpenAI’s TTS system and played back to the user.
- **Step 5**: The assistant continues to loop, capturing the screen and awaiting further voice commands.

---

## Usage Example

### 1. Ask the assistant: 
   "What’s on my screen right now?"

   - The assistant will capture the current screenshot, process the prompt, and respond based on the desktop content. For example:
   
   **User Prompt**: "What is this webpage showing?"

   **Assistant Response**: "This webpage is showing a news article about AI advancements."

### 2. Ask a factual question: 
   "What time is it?"

   - The assistant will provide an immediate answer.

---

## Known Issues

- **Audio Recognition Errors**: In environments with too much background noise, the speech recognition may not perform optimally.
- **High CPU Usage**: Continuous screenshot capture at 0.1-second intervals may lead to higher CPU usage.
- **TTS Latency**: There might be a slight delay in generating and playing audio responses, depending on the network speed for API calls.

---

## Future Enhancements

- **Multilingual Support**: Add support for multiple languages in both speech recognition and responses.
- **Improved Screenshot Capture**: Optimize CPU usage by dynamically adjusting the screenshot capture interval based on system load.
- **Additional Tools**: Integrate more AI tools, like GPT-4, for enhanced question answering capabilities.

---

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it as per the terms of the license.
---
