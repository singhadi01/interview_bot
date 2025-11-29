def tts_play(question):
    import edge_tts
    import asyncio
    import tempfile
    import pathlib
    VOICE = "en-US-AriaNeural"
    async def speak(text):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            output = tmp.name
        tts = edge_tts.Communicate(text, VOICE)
        await tts.save(output)
        from playsound import playsound
        playsound(output)
        pathlib.Path(output).unlink(missing_ok=True)

    asyncio.run(speak(question))

