# src/atc2txt/lib/run_server.py


def run_server(model):
    print("Run server with model:", model)

    from atc2txt.lib.server import TranscriptionServer

    server = TranscriptionServer()
    server.run(
        "0.0.0.0",
        port=9090,
        faster_whisper_custom_model_path=model,
    )
