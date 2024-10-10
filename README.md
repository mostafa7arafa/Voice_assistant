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
