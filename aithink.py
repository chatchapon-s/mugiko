import speech_recognition as sr
import openai
import requests
import pygame
import io
import re
pygame.init()

openai.api_key = "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"

def generate_response(input_text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"คุณชื่อ Mugiko รับคำสั่ง: \"{input_text}\"",
        max_tokens=2048,
        temperature=0.5
    )
    short_text(response.choices[0].text.strip())
    return response.choices[0].text.strip()


def short_text(text):
    # แบ่งข้อความเป็นคำๆ
    words = re.findall(r'\S+', text)

    # แบ่งข้อความออกเป็นส่วนๆ ที่มีความยาวไม่เกิน 200 ตัวอักษร
    max_length = 200
    chunks = []
    current_chunk = ""

    for word in words:
        if len(current_chunk) + len(word) + 1 <= max_length:
            current_chunk += word + " "
        else:
            chunks.append(current_chunk)
            current_chunk = word + " "

    if current_chunk:
        chunks.append(current_chunk)

    for chunk in chunks:
        chunk = chunk.strip()
        if chunk:
            text_to_speech(chunk)
            print("Response chunk:", chunk)


def text_to_speech(text):
    # URL ของ API
    url = "https://translate.google.com/translate_tts?ie=UTF-8"

    # พารามิเตอร์ที่จำเป็น
    params = {
        "q": text,
        "tl": "th-TH",
        "client": "tw-ob"
    }

    # ส่งคำขอ GET ไปยัง API
    response = requests.get(url, params=params)

    # ตรวจสอบว่าคำขอสำเร็จหรือไม่
    if response.status_code == 200:
        # สร้างเสียงจากข้อมูลเสียง
        sound = pygame.mixer.Sound(io.BytesIO(response.content))

        # เล่นเสียงด้วย pygame
        pygame.mixer.music.load(io.BytesIO(response.content))
        pygame.mixer.music.play()

        # รอจนกว่าเสียงจะเล่นเสร็จ
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
    else:
        print("เกิดข้อผิดพลาดในการเรียก API")

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")

        try:
            audio = r.listen(source)
            text = r.recognize_google(audio, language='th-TH')
            print("You said (in Thai):", text)
            return text

        except sr.UnknownValueError:
            try:
                audio = r.listen(source)
                text = r.recognize_google(audio, language='en-US')
                print("You said (in English):", text)
                return text

            except sr.UnknownValueError:
                print("Sorry, I couldn't understand.")
                return None

        except sr.RequestError as e:
            print("Sorry, I encountered an error:", str(e))
            return None