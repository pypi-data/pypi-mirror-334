# src/atc2txt/lib/run_client.py

from atc2txt.lib.client import TranscriptionClient

def run_client(url, model):
    print("Run client with url:", url)

    client = TranscriptionClient(
    "localhost",
    9090,
    lang="en",
    translate=False,
    model=model,
    max_clients=4,
    max_connection_time=600,
    mute_audio_playback=True,
    )

    client(mp3_url=url)
