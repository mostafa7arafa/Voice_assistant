import base64
import logging
from threading import Lock, Thread
import time
import numpy
import cv2
import openai
from PIL import ImageGrab
from cv2 import imencode
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.messages import SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from pyaudio import PyAudio, paInt16
from speech_recognition import Microphone, Recognizer, UnknownValueError

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DesktopScreenshot:
    def __init__(self):
        self.screenshot = None
        self.running = False
        self.lock = Lock()

    def start(self):
        if self.running:
            return self

        logger.info("Starting Desktop Screenshot thread.")
        self.running = True
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True  # Ensure thread exits when main program does
        self.thread.start()
        return self

    def update(self):
        while self.running:
            try:
                screenshot = ImageGrab.grab()
                screenshot = cv2.cvtColor(numpy.array(screenshot), cv2.COLOR_RGB2BGR)

                with self.lock:
                    self.screenshot = screenshot

                logger.debug("Screenshot updated.")  # Log when screenshot is updated
                time.sleep(0.1)  # Short sleep to reduce CPU usage
            except Exception as e:
                logger.error(f"Error in screenshot thread: {e}")

    def read(self, encode=False):
        with self.lock:
            screenshot = self.screenshot.copy() if self.screenshot is not None else None

        if encode and screenshot is not None:
            _, buffer = imencode(".jpeg", screenshot)
            return base64.b64encode(buffer)

        return screenshot

    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()
        logger.info("Desktop Screenshot thread stopped.")


class Assistant:
    def __init__(self, model):
        self.chain = self._create_inference_chain(model)

    def answer(self, prompt, image):
        if not prompt:
            return

        logger.info(f"Prompt received: {prompt}")

        try:
            response = self.chain.invoke(
                {"prompt": prompt, "image_base64": image.decode()},
                config={"configurable": {"session_id": "unused"}},
            ).strip()

            logger.info(f"Response generated: {response}")

            if response:
                self._tts(response)
        except Exception as e:
            logger.error(f"Error in generating response: {e}")

    def _tts(self, response):
        player = PyAudio().open(format=paInt16, channels=1, rate=24000, output=True)

        try:
            with openai.audio.speech.with_streaming_response.create(
                model="tts-1",
                voice="shimmer",
                response_format="pcm",
                input=response,
            ) as stream:
                for chunk in stream.iter_bytes(chunk_size=1024):
                    player.write(chunk)
        except Exception as e:
            logger.error(f"Error in TTS: {e}")

    def _create_inference_chain(self, model):
        SYSTEM_PROMPT = """
        You are a witty assistant that will use the chat history and the image 
        provided by the user to answer its questions.

        Use few words on your answers. Go straight to the point. Do not use any
        emoticons or emojis. Do not ask the user any questions.

        Be friendly and helpful. Show some personality. Do not be too formal.
        """

        prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="chat_history"),
                (
                    "human",
                    [
                        {"type": "text", "text": "{prompt}"},
                        {
                            "type": "image_url",
                            "image_url": "data:image/jpeg;base64,{image_base64}",
                        },
                    ],
                ),
            ]
        )

        chain = prompt_template | model | StrOutputParser()

        chat_message_history = ChatMessageHistory()
        return RunnableWithMessageHistory(
            chain,
            lambda _: chat_message_history,
            input_messages_key="prompt",
            history_messages_key="chat_history",
        )


desktop_screenshot = DesktopScreenshot().start()

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")
assistant = Assistant(model)

def audio_callback(recognizer, audio):
    try:
        prompt = recognizer.recognize_whisper(audio, model="base", language="english")
        assistant.answer(prompt, desktop_screenshot.read(encode=True))
    except UnknownValueError:
        logger.warning("There was an error processing the audio.")
    except Exception as e:
        logger.error(f"Error in audio callback: {e}")

recognizer = Recognizer()
microphone = Microphone()
with microphone as source:
    logger.info("Adjusting for ambient noise.")
    recognizer.adjust_for_ambient_noise(source)

stop_listening = recognizer.listen_in_background(microphone, audio_callback)

try:
    while True:
        screenshot = desktop_screenshot.read()
        if screenshot is not None:
            # cv2.imshow("Desktop", screenshot)
            pass
        else:
            logger.warning("No screenshot captured.")

        if cv2.waitKey(1) in [27, ord("q")]:  # Exit on 'Esc' or 'q'
            logger.info("Exiting main loop.")
            break
        time.sleep(0.1)  # Adding a small delay to avoid tight loop
except Exception as e:
    logger.error(f"Error in the main loop: {e}")
finally:
    desktop_screenshot.stop()
    cv2.destroyAllWindows()
    stop_listening(wait_for_stop=False)
    logger.info("Application stopped.")