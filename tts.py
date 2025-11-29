def tts_play(question):
    import pyttsx3
    import pythoncom
    pythoncom.CoInitialize() 
    engine = pyttsx3.init()
    engine.setProperty('rate', 140)
    engine.say(question)
    engine.runAndWait()
    
