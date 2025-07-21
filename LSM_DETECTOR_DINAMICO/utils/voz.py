import pyttsx3

def decir(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()
