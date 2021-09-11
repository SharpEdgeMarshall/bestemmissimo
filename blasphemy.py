import requests


def _get_text_blasphemy() -> str:
    res = requests.get("https://bestemmiajouer.herokuapp.com/api/generate?len=1")
    return res.json()["text"]


def _get_tts(text: str):
    qs = {"text": text}
    res = requests.get(
        "https://bestemmiajouer.herokuapp.com/api/tts", params=qs, stream=True
    )
    return res.raw


def generate_graphic_blasphemy():
    pass


def generate_blasphemy() -> str:
    return _get_text_blasphemy()


def generate_audio_blasphemy():
    return _get_tts(_get_text_blasphemy())
