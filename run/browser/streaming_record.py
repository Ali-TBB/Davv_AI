import speech_recognition as sr


def detect(on_detect: callable):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Listening for 'Hi Gemini'...")

    while True:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            # Use PocketSphinx for offline recognition
            command = recognizer.recognize_google(audio).lower()
            print(f"Recognized: {command}")

            if "hi google" in command or "hey google" in command:
                print("Trigger word detected. Starting recording...")
                on_detect()
                break

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
